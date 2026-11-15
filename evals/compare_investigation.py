"""Transparent synthetic comparison: single-message validation vs investigation.

This is not evidence of real-world bank investigation accuracy.
Run: python -m evals.compare_investigation
"""
from __future__ import annotations
from iso20022_mcp import generate, parser, validate
from iso20022_mcp.investigate import investigate_payment


def examples():
    scenarios = [
        ("known_reject_AC04", "AC04", False, "matched", "RJCT"),
        ("known_reject_AM05", "AM05", False, "matched", "RJCT"),
        ("unknown_reason_ZZ99", "ZZ99", False, "matched", "RJCT"),
        ("group_id_mismatch", "AC04", True, "unmatched", None),
    ]
    for label, reason, mismatch, expected_match, expected_status in scenarios:
        xml8 = generate.generate_pacs008()
        p = parser.parse_message(xml8)
        tx = p["transactions"][0]
        xml2 = generate.generate_pacs002(
            reason_code=reason,
            original_msg_id=("NOT-" + p["msg_id"]) if mismatch else p["msg_id"],
            end_to_end_id=tx["end_to_end_id"],
        )
        yield label, xml8, xml2, expected_match, expected_status


def run():
    records = []
    for name, xml8, xml2, expected_match, expected_status in examples():
        baseline = validate.validate_message(xml8)
        report = investigate_payment(xml8, xml2)
        case = report["cases"][0]
        # A single-message baseline cannot verify bank response correlation.
        baseline_correct = (
            expected_match == "unmatched" and expected_status is None
            and not baseline["business_valid"]
        )
        investigation_correct = (
            case["correlation"] == expected_match
            and case["reported_status"] == expected_status
            and case["decision"] == "no_automatic_retry_or_mutation"
        )
        if name == "unknown_reason_ZZ99":
            investigation_correct = investigation_correct and (
                case["reported_reasons"][0]["reported_meaning"] is None
            )
        records.append((name, baseline_correct, investigation_correct))
    print("CASE                          SINGLE_XML_ONLY  EVIDENCE_INVESTIGATION")
    for name, baseline, investigated in records:
        print(f"{name:<29} {str(baseline):<16} {investigated}")
    print(f"Total correct for these {len(records)} synthetic cases: "
          f"{sum(a for _, a, _ in records)}/{len(records)} baseline; "
          f"{sum(b for _, _, b in records)}/{len(records)} investigation")
    return records


if __name__ == "__main__":
    run()
