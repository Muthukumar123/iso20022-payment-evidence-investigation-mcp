"""Assert documented synthetic benchmark CLI executes and reports its limits."""
from pathlib import Path
import subprocess
import sys


def test_synthetic_evidence_comparison():
    script = Path(__file__).resolve().parents[1] / "evals" / "compare_investigation.py"
    result = subprocess.run(
        [sys.executable, str(script)], check=True, capture_output=True, text=True
    )
    assert "Total correct for these 4 synthetic cases:" in result.stdout
    assert "4/4 investigation" in result.stdout
