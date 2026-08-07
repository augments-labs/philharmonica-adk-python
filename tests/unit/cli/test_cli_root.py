"""Tests for the ``philharmonica`` root command group."""

from __future__ import annotations

import subprocess
import sys

from click.testing import CliRunner

from philharmonica.adk import __version__
from philharmonica.adk.cli import main


def test_help_exits_zero() -> None:
    result = CliRunner().invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "philharmonica" in result.output


def test_version_prints_package_version() -> None:
    result = CliRunner().invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_python_dash_m_entry_point() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "philharmonica.adk.cli", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "philharmonica" in proc.stdout
