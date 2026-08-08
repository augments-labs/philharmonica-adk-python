"""Offline unit tests for PgVectorStore (no DB needed)."""

from __future__ import annotations

from typing import Any

import pytest

pytest.importorskip("pgvector")
pytest.importorskip("psycopg")

from philharmonica.adk.memory import MemoryMetadata, MemorySource
from philharmonica.adk.memory.stores.pgvector import PgVectorStore, _row_to_record
from philharmonica.adk.memory.vector_store import VectorRecord


@pytest.mark.parametrize("bad", ["", "a" * 65, "bad-name", "123start", "drop;table", "has space"])
def test_rejects_bad_table_name(bad: str) -> None:
    with pytest.raises(ValueError, match="table name"):
        PgVectorStore(conninfo="postgresql://fake", dimensions=2, table=bad)


def test_rejects_nonpositive_dimensions() -> None:
    with pytest.raises(ValueError, match="dimensions"):
        PgVectorStore(conninfo="postgresql://fake", dimensions=0, table="memory_vectors")


def test_accepts_valid_table_name() -> None:
    # Construction with a valid identifier must NOT raise (no DB connection happens in __init__).
    store = PgVectorStore(conninfo="postgresql://fake", dimensions=2, table="memory_vectors")
    assert store is not None


class _CaptureConn:
    """Async connection stub that records the SQL it is asked to execute."""

    def __init__(self) -> None:
        self.statements: list[str] = []

    async def execute(self, statement: Any, params: Any | None = None) -> None:
        self.statements.append(statement.as_string())

    async def __aenter__(self) -> _CaptureConn:
        return self

    async def __aexit__(self, *exc: object) -> bool:
        return False


class _CapturePool:
    """Pool stub whose ``connection()`` yields the capturing connection."""

    def __init__(self, conn: _CaptureConn) -> None:
        self._conn = conn

    def connection(self) -> _CaptureConn:
        return self._conn


async def test_upsert_sql_refreshes_namespace_on_conflict(monkeypatch: pytest.MonkeyPatch) -> None:
    # Replacing a record under a new namespace must overwrite the stored
    # namespace, so the ON CONFLICT clause has to update it alongside content.
    store = PgVectorStore(conninfo="postgresql://fake", dimensions=2, table="memory_vectors")
    conn = _CaptureConn()

    async def _fake_ensure_ready() -> _CapturePool:
        return _CapturePool(conn)

    monkeypatch.setattr(store, "_ensure_ready", _fake_ensure_ready)
    record = VectorRecord(
        id="a",
        vector=[1.0, 0.0],
        namespace="u1",
        content="a",
        metadata=MemoryMetadata(source=MemorySource.MANUAL),
        created_at=1.0,
        updated_at=1.0,
    )
    await store.upsert([record])

    assert len(conn.statements) == 1
    statement = conn.statements[0]
    assert "ON CONFLICT (id) DO UPDATE" in statement
    assert "namespace = EXCLUDED.namespace" in statement


class _VectorWithToList:
    """Stand-in for the pgvector >= 0.5 ``Vector``: exposes ``to_list()``, is not iterable."""

    def __init__(self, values: list[float]) -> None:
        self._values = values

    def to_list(self) -> list[float]:
        return self._values


def _row(embedding: object) -> tuple[object, ...]:
    # Column order is fixed by every SELECT in the store module:
    # id, namespace, content, metadata, embedding, created_at, updated_at.
    return ("m1", "u1", "hello", {}, embedding, 1.0, 2.0)


def test_row_decodes_embedding_exposing_to_list() -> None:
    # pgvector >= 0.5 hands back a Vector that cannot be iterated directly, so
    # the decoder has to go through to_list() rather than tuple(...) it.
    record = _row_to_record(_row(_VectorWithToList([1.0, 0.0])))

    assert record.vector == (1.0, 0.0)


def test_row_decodes_embedding_already_a_sequence() -> None:
    # pgvector 0.4 (and a plain list column) yield something already iterable.
    record = _row_to_record(_row([0.5, 0.25]))

    assert record.vector == (0.5, 0.25)


def test_row_decodes_remaining_columns_by_position() -> None:
    record = _row_to_record(_row([1.0, 0.0]))

    assert (record.id, record.namespace, record.content) == ("m1", "u1", "hello")
    assert (record.created_at, record.updated_at) == (1.0, 2.0)
