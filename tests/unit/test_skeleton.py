"""Smoke test for package skeleton (milestone C0)."""

from a615a_sim import __version__
from a615a_sim.cli import main


def test_version():
    assert __version__ == "0.0.1"


def test_cli_exits_zero():
    assert main([]) == 0
