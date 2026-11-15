"""Gamma publishing must remain offline and fail-closed by default."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "publish_gamma.py"


def invoke(*args):
    env = os.environ.copy()
    env.pop("GAMMA_API_KEY", None)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], cwd=ROOT,
        env=env, capture_output=True, text=True, timeout=10,
    )


def test_dry_run_builds_private_ten_card_payload():
    result = invoke("--dry-run")
    assert result.returncode == 0, result.stderr
    metadata = json.loads(result.stdout)
    assert metadata["cards"] == 10
    assert metadata["mode"] == "offline-dry-run"
    assert metadata["externalAccess"] == "noAccess"


def test_default_mode_is_offline():
    result = invoke()
    assert result.returncode == 0
    assert "offline-dry-run" in result.stdout


def test_publish_requires_confirmation():
    result = invoke("--publish")
    assert result.returncode == 1
    assert "confirm-external-generation" in result.stderr


def test_publish_requires_secret_before_any_http():
    result = invoke("--publish", "--confirm-external-generation")
    assert result.returncode == 1
    assert "GAMMA_API_KEY is missing" in result.stderr


def test_presentation_contains_exactly_ten_synthetic_cards():
    source = ROOT / "docs/finserv/GAMMA_EXECUTIVE_DECK.md"
    contents = source.read_text(encoding="utf-8")
    assert contents.count("\n---\n") == 9
    assert "No autonomous retry" in contents
    assert "No direct AI-to-core banking connectivity" in contents
