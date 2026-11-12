"""Evidence-first pacs.008 / pacs.002 investigation.

No LLM, payment authorization, bank connectivity, or mutation. A reported
reason code is evidence about a bank's status response, not independent proof
about a beneficiary account or payment-rail state.
"""
from __future__ import annotations

import re
from .parser import parse_message
from .validate import validate_message
from .codes import lookup_code, REPAIR_HINT

PAYMENT_REF_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")


def _evidence(source: str, path: str, value: str | None, statement: str) -> dict:
    return {
        "source": source,
        "field": path,
        "value": value,
        "statement": statement,
    }


def _recommended_action(status: str | None, reason: str | None) -> str:
    if status != "RJCT":
        return "Review the authoritative payment-hub state before deciding on a retry."
    if reason in REPAIR_HINT:
        return REPAIR_HINT[reason] + " Require an authorized human decision before any resubmission."
    return (
        "Investigate the original bank response and official scheme rules. "
        "Do not change or resend the payment automatically."
    )


def _matches(payment: dict, status: dict) -> bool:
    """Require an explicit identifier; reject conflicting identifiers."""
    e2e = status.get("original_end_to_end_id")
    uetr = status.get("original_uetr")
    if not e2e and not uetr:
        return False
    if e2e and e2e != payment.get("end_to_end_id"):
        return False
    if uetr and uetr != payment.get("uetr"):
        return False
    return True


def investigate_payment(pacs008_xml: str, pacs002_xml: str) -> dict:
    """Correlate two supplied messages and produce evidence-backed findings.

    Does not infer correlation from names, amounts, or fuzzy matching.
    Reported reasons are kept separate from hypothesized underlying causes.
    """
    original = parse_message(pacs008_xml)
    response = parse_message(pacs002_xml)
    if original["message_type"] != "pacs.008":
        raise ValueError("First message must be pacs.008.")
    if response["message_type"] != "pacs.002":
        raise ValueError("Second message must be pacs.002.")

    orig_validation = validate_message(pacs008_xml)
    status_validation = validate_message(pacs002_xml)
    cases: list[dict] = []
    observed_indices: set[int] = set()
    group_matches = (
        bool(response["original_msg_id"])
        and response["original_msg_id"] == original["msg_id"]
    )

    for index, payment in enumerate(original["transactions"]):
        e2e_id = payment.get("end_to_end_id")
        uetr = payment.get("uetr")
        base_evidence = [
            _evidence("pacs.008", f"CdtTrfTxInf[{index}]/PmtId/EndToEndId",
                      e2e_id, "Original payment identifier"),
            _evidence("pacs.008", f"CdtTrfTxInf[{index}]/PmtId/UETR",
                      uetr, "Original unique end-to-end transaction reference"),
        ]
        matches = [
            (i, transaction) for i, transaction in enumerate(response["transactions"])
            if group_matches and _matches(payment, transaction)
        ]
        match_status = "matched" if len(matches) == 1 else (
            "ambiguous" if len(matches) > 1 else "unmatched"
        )
        reason_details = []
        reported_status = None
        assessment = "No conclusively correlated bank status report was provided."
        safety = "human_review_required"
        recommendation = (
            "Confirm the status through an authorized payment hub. "
            "Do not retry an unconfirmed payment."
        )
        evidence = list(base_evidence)
        if len(matches) == 1:
            status_index, tx_status = matches[0]
            observed_indices.add(status_index)
            reported_status = tx_status.get("status")
            evidence.extend([
                _evidence("pacs.002", "OrgnlGrpInfAndSts/OrgnlMsgId",
                          response["original_msg_id"],
                          "Original-message identifier matches pacs.008"),
                _evidence("pacs.002", f"TxInfAndSts[{status_index}]/TxSts",
                          reported_status, "Bank-reported transaction status"),
            ])
            for reason_index, reason in enumerate(tx_status["reasons"]):
                code = reason.get("code")
                code_info = lookup_code(code or "")
                reason_details.append({
                    "code": code,
                    "found_in_local_table": code_info["found"],
                    "reported_meaning": code_info.get("meaning"),
                    "interpretation_limit": (
                        "Bank-reported reason; not independent verification of the "
                        "underlying account or rail condition."
                    ),
                })
                evidence.append(_evidence(
                    "pacs.002",
                    f"TxInfAndSts[{status_index}]/StsRsnInf[{reason_index}]/Rsn/Cd",
                    code, "Bank-provided status reason code",
                ))
            if reported_status == "RJCT":
                if not reason_details:
                    assessment = (
                        "Bank reports rejection, but no machine-readable "
                        "reason code is present."
                    )
                elif any(not r["found_in_local_table"] for r in reason_details):
                    assessment = (
                        "Bank reports rejection; at least one reason code is "
                        "not in the local reference table. No meaning inferred."
                    )
                else:
                    assessment = "Bank reports rejection with mapped reason code(s)."
            else:
                assessment = (
                    "A correlated status message was found; do not infer rejection "
                    "unless its status is RJCT."
                )
            first_code = reason_details[0]["code"] if reason_details else None
            recommendation = _recommended_action(reported_status, first_code)
            unsafe = (
                orig_validation["security_status"] != "clear"
                or status_validation["security_status"] != "clear"
            )
            safety = "human_review_required" if unsafe or reported_status == "RJCT" else "read_only"
        cases.append({
            "end_to_end_id": e2e_id,
            "uetr": uetr,
            "correlation": match_status,
            "reported_status": reported_status,
            "reported_reasons": reason_details,
            "assessment": assessment,
            "recommended_action": recommendation,
            "decision": "no_automatic_retry_or_mutation",
            "workflow": safety,
            "evidence": evidence,
        })

    if not group_matches:
        correlation_note = (
            "pacs.002 original message ID does not match pacs.008 message ID. "
            "No transaction status was attributed to the original payment."
        )
    else:
        correlation_note = "Group identifier matches; correlation also requires exact transaction IDs."
    unmatched_statuses = [
        i for i in range(len(response["transactions"])) if i not in observed_indices
    ]

    return {
        "analysis_type": "deterministic_evidence_based_investigation",
        "read_only": True,
        "payment_msg_id": original["msg_id"],
        "status_msg_id": response["msg_id"],
        "group_correlation": group_matches,
        "correlation_note": correlation_note,
        "original_validation": {
            "business_valid": orig_validation["business_valid"],
            "security_status": orig_validation["security_status"],
            "schema_status": orig_validation["schema_status"],
        },
        "status_validation": {
            "business_valid": status_validation["business_valid"],
            "security_status": status_validation["security_status"],
            "schema_status": status_validation["schema_status"],
        },
        "cases": cases,
        "unmatched_status_transaction_indices": unmatched_statuses,
        "limitations": [
            "No live bank connectivity or payment execution.",
            "No authoritative account-status verification.",
            "No CBPR+, SEPA, or rail-specific rule decision.",
            "Neither a valid XML document nor a mapped reason code authorizes a retry.",
        ],
    }
