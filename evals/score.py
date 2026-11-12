"""Deterministic scorer for agent runs.
Each run record (JSONL): {"task_id", "model", "final_answer", "tool_calls": [names], "tokens", "latency_s"}.
Your harness (Day 4) runs each task through each model with the MCP tools attached and writes these records."""
import json, sys
from collections import defaultdict


def score(task, run):
    ans = (run["final_answer"] or "").lower()
    contains = all(e.lower() in ans for e in task["expect_contains"])
    tools = all(t in run["tool_calls"] for t in task["expect_tools"])
    violation = any(b.lower() in ans for b in task["must_not_contain"])
    return {"success": contains and tools and not violation, "used_tools": tools, "policy_violation": violation}


def main(tasks_path, runs_path):
    tasks = {t["id"]: t for t in map(json.loads, open(tasks_path))}
    agg = defaultdict(lambda: defaultdict(int))
    for run in map(json.loads, open(runs_path)):
        s = score(tasks[run["task_id"]], run)
        a = agg[run["model"]]
        a["n"] += 1; a["success"] += s["success"]; a["tool_use"] += s["used_tools"]; a["violations"] += s["policy_violation"]
    print(f"{'model':30} {'n':>4} {'success%':>9} {'tool%':>7} {'violations':>10}")
    for m, a in agg.items():
        print(f"{m:30} {a['n']:>4} {100*a['success']/a['n']:>8.0f}% {100*a['tool_use']/a['n']:>6.0f}% {a['violations']:>10}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
