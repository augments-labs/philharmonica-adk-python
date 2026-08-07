.PHONY: sync coverage coverage-html coverage-integration coverage-full typecheck typecheck-fast typecheck-changed

# How every tool below is invoked. `uv run` resolves the locked environment in
# .venv, creating it on first use. Override with an empty value to run against
# whatever interpreter is already active (e.g. the conda env from
# environment.yaml):  make typecheck-fast RUN=
RUN ?= uv run

# Create/update .venv from uv.lock with the dev toolchain. `uv run` does this
# implicitly, so this target is only needed to warm the environment up front
# or to point an editor at .venv.
sync:
	uv sync --extra dev

# Fast inner-loop gate: mypy only (canonical; matches the per-PR CI gate).
typecheck-fast:
	$(RUN) mypy -p philharmonica.adk

# Inner-loop gate WITH pyright signal, without the slow whole-tree run: mypy
# (canonical) + pyright scoped to the src files you changed (staged, unstaged,
# and untracked). Fast for typical edits; only slow if you changed the heavy
# run/graph/swarm core, which pulls in the framework's full type graph.
typecheck-changed: typecheck-fast
	@files=$$( { git diff --name-only --diff-filter=ACMR; git diff --name-only --cached --diff-filter=ACMR; git ls-files --others --exclude-standard; } | sort -u | grep -E '^src/.*\.py$$' ); \
	if [ -n "$$files" ]; then \
		echo "pyright (changed src files):"; echo "$$files" | sed 's/^/  /'; \
		$(RUN) pyright $$files; \
	else \
		echo "pyright: no changed src .py files"; \
	fi

# Full type-check: mypy + full pyright. pyright re-analyses the framework's
# heavy core (run/graph/swarm) type graph and is slow (~30 min, hours under IDE
# langserver contention) — CI runs it nightly, not per-PR. For the inner loop
# prefer `make typecheck-fast` (mypy) or `make typecheck-changed` (mypy +
# pyright on just your changes).
typecheck: typecheck-fast
	$(RUN) pyright src/philharmonica/adk/

# Self-contained unit coverage — mirrors the per-PR CI gate (ci.yml "Unit
# tests"). LLMs are mocked and fakeredis/moto/embedded stores keep it offline,
# so no DB, services, or API keys are needed. Postgres-backed unit tests are
# deselected by marker (they run in integration.yml); --reruns 2 absorbs two known
# timing-flaky tests. The coverage.report fail_under gate applies automatically.
coverage:
	$(RUN) pytest tests/unit -m "not integration and not postgres" -n auto --dist loadfile --reruns 2 --cov=src/philharmonica --cov-report=term-missing

# Same self-contained run, plus a browsable HTML report.
coverage-html:
	$(RUN) pytest tests/unit -m "not integration and not postgres" -n auto --dist loadfile --reruns 2 --cov=src/philharmonica --cov-report=html --cov-report=term-missing
	@echo "HTML report: .coverage/html/index.html"

# Unit + integration coverage in one combined number (coverage.run parallel=true
# merges the -n auto workers), plus a browsable HTML report. REQUIRES local
# infra, unlike `coverage`:
#   - Postgres+pgvector on :5432 with the `vector` extension and the PG *server*
#     binaries on PATH, plus PHILHARMONICA_TEST_PG_DSN
#     (e.g. postgresql://postgres:postgres@localhost:5432/philharmonica_test)
#   - Redis on :6379, plus PHILHARMONICA_TEST_REDIS_URL (e.g. redis://localhost:6379/0)
#   - a running Docker daemon and `uv sync --extra dev --extra sandbox-docker`
# Live-LLM e2e is EXCLUDED here (-m "not e2e"); use `coverage-full` to add it.
coverage-integration:
	$(RUN) pytest tests/unit tests/integration -m "not e2e" -n auto --dist loadfile --cov=src/philharmonica --cov-report=html --cov-report=term-missing
	@echo "HTML report: .coverage/html/index.html"

# Everything, including live-LLM e2e (tests/integration/llms), plus a browsable
# HTML report. Needs coverage-integration's infra PLUS real provider keys from a
# gitignored .env (cp .env.example .env). The suite does not auto-load .env, so
# this sources it for the run. Hits real provider APIs — costs money. Without
# keys the e2e tests skip; with fake keys they fail on auth, so use real keys or
# none.
coverage-full:
	set -a; [ -f .env ] && . ./.env; set +a; $(RUN) pytest tests/unit tests/integration -n auto --dist loadfile --cov=src/philharmonica --cov-report=html --cov-report=term-missing
	@echo "HTML report: .coverage/html/index.html"
