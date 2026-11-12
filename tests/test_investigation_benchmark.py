"""Benchmark assertions demonstrate capabilities, not field accuracy."""
from evals.compare_investigation import run


def test_synthetic_evidence_comparison():
    scenarios = run()
    assert len(scenarios) == 4
    assert all(not baseline for _, baseline, _ in scenarios)
    assert all(engine for _, _, engine in scenarios)
