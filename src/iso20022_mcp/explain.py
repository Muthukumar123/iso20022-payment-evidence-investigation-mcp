"""Deterministic plain-language summaries (no LLM involved, so nothing is invented)."""
from .parser import parse_message
from .codes import lookup_code


def explain_message(xml: str) -> str:
    m = parse_message(xml)
    lines = [f"{m['message_type']} message {m['msg_id']} created {m['created']}, {m['actual_tx_count']} transaction(s)."]
    for i, tx in enumerate(m["transactions"], 1):
        if m["message_type"] == "pacs.008":
            d, c = tx["debtor"], tx["creditor"]
            lines.append(
                f"{i}. {d['name']} ({d['iban']}, bank {d['agent_bic']}) pays {tx['amount']} {tx['currency']} "
                f"to {c['name']} ({c['iban']}, bank {c['agent_bic']}) on {tx['settlement_date']}; "
                f"charges: {tx['charge_bearer']}; reference {tx['end_to_end_id']}.")
            if tx["remittance_unstructured_UNTRUSTED"]:
                lines.append("   Remittance text (untrusted, quoted verbatim): " +
                             " | ".join(repr(t) for t in tx["remittance_unstructured_UNTRUSTED"]))
        else:
            reasons = "; ".join(f"{r['code']}: {lookup_code(r['code']).get('meaning') or 'unknown code'}"
                                for r in tx["reasons"]) or "none given"
            lines.append(f"{i}. Payment {tx['original_end_to_end_id']} from {m['original_msg_id']} "
                         f"has status {tx['status']}. Reasons: {reasons}.")
    return "\n".join(lines)
