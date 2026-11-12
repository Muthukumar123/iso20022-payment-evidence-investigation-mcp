"""Business-rule validation. XSD validation can be layered on once official schemas are added."""
from __future__ import annotations
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .parser import parse_message, ParseError
from .codes import CHARGE_BEARER, STATUS_REASON, TX_STATUS
from .currency import currency_decimals
from .schema import validate_schema

BIC_RE = re.compile(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$")
UETR_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", re.I)
# Country-specific length checks, in addition to ISO IBAN mod-97.
IBAN_LENGTHS = {
    "AD": 24, "AE": 23, "AL": 28, "AT": 20, "AZ": 28, "BA": 20,
    "BE": 16, "BG": 22, "BH": 22, "BR": 29, "BY": 28, "CH": 21,
    "CR": 22, "CY": 28, "CZ": 24, "DE": 22, "DK": 18, "DO": 28,
    "EE": 20, "EG": 29, "ES": 24, "FI": 18, "FO": 18, "FR": 27,
    "GB": 22, "GE": 22, "GI": 23, "GL": 18, "GR": 27, "GT": 28,
    "HR": 21, "HU": 28, "IE": 22, "IL": 23, "IQ": 23, "IS": 26,
    "IT": 27, "JO": 30, "KW": 30, "KZ": 20, "LB": 28, "LI": 21,
    "LT": 20, "LU": 20, "LV": 21, "MC": 27, "MD": 24, "ME": 22,
    "MK": 19, "MR": 27, "MT": 31, "MU": 30, "NL": 18, "NO": 15,
    "PK": 24, "PL": 28, "PS": 29, "PT": 25, "QA": 29, "RO": 24,
    "RS": 22, "SA": 24, "SC": 31, "SE": 24, "SI": 19, "SK": 24,
    "SM": 27, "ST": 25, "SV": 28, "TL": 23, "TN": 24, "TR": 26,
    "UA": 29, "VA": 22, "VG": 24, "XK": 20,
}
INJECTION_RE = re.compile(
    r"(ignore (all |any )?(previous|prior)? ?instructions|system prompt|you are now|disregard .{0,30}(rules|policy)|"
    r"approve (this|the) payment|change the (iban|beneficiary|amount)|<\s*/?\s*(tool|instruction)s?\s*>)", re.I)


def iban_ok(iban: str) -> bool:
    s = (iban or "").replace(" ", "").upper()
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{11,30}", s):
        return False
    expected = IBAN_LENGTHS.get(s[:2])
    if expected is not None and len(s) != expected:
        return False
    return int("".join(str(int(ch, 36)) for ch in s[4:] + s[:4])) % 97 == 1


def _issue(sev, field, msg, code=None):
    d = {"severity": sev, "field": field, "message": msg}
    if code:
        d["likely_reject_code"] = code
    return d


def validate_message(xml: str) -> dict:
    try:
        m = parse_message(xml)
    except ParseError as e:
        return {
            "valid": False, "business_valid": False, "schema_valid": False,
            "schema_status": "not_evaluated", "schema_issues": [],
            "security_status": "not_evaluated", "conformant": False,
            "message_type": None, "message_version": None,
            "issues": [_issue("error", "document", str(e), "FF01")],
        }
    schema_result = validate_schema(xml, m["namespace"])
    issues = []
    if not m["msg_id"]:
        issues.append(_issue("error", "GrpHdr/MsgId", "Message ID missing."))
    elif len(m["msg_id"]) > 35:
        issues.append(_issue("error", "GrpHdr/MsgId", "Message ID longer than 35 characters."))
    try:
        datetime.fromisoformat((m["created"] or "").replace("Z", "+00:00"))
    except ValueError:
        issues.append(_issue("error", "GrpHdr/CreDtTm", "Creation date-time missing or not ISO 8601."))
    if m["message_type"] == "pacs.008" and not m["declared_tx_count"]:
        issues.append(_issue("error", "GrpHdr/NbOfTxs", "Transaction count missing."))
    elif m["declared_tx_count"] is not None:
        count = m["declared_tx_count"]
        if not re.fullmatch(r"[0-9]+", count) or int(count) <= 0:
            issues.append(_issue("error", "GrpHdr/NbOfTxs", "Transaction count must be positive."))
        elif int(count) != m["actual_tx_count"]:
            issues.append(_issue("error", "GrpHdr/NbOfTxs",
                                 f"Declares {count} transactions but contains {m['actual_tx_count']}."))
    if m["message_type"] == "pacs.008" and m["actual_tx_count"] == 0:
        issues.append(_issue("error", "CdtTrfTxInf", "At least one transaction required."))

    for i, tx in enumerate(m["transactions"]):
        p = f"tx[{i}]"
        if m["message_type"] == "pacs.008":
            if not tx["end_to_end_id"]:
                issues.append(_issue("error", f"{p}/EndToEndId", "EndToEndId missing."))
            if tx["uetr"] and not UETR_RE.fullmatch(tx["uetr"]):
                issues.append(_issue("error", f"{p}/UETR", "UETR is not a valid UUID v4."))
            try:
                amt = Decimal(tx["amount"] or "")
                if not amt.is_finite():
                    raise InvalidOperation("Non-finite amount")
                if amt <= 0:
                    issues.append(_issue("error", f"{p}/Amount", "Amount must be positive."))
                allowed = currency_decimals(tx["currency"] or "")
                if allowed is not None and -amt.as_tuple().exponent > allowed:
                    issues.append(_issue("error", f"{p}/Amount", f"{tx['currency']} allows at most {allowed} decimals."))
            except InvalidOperation:
                issues.append(_issue("error", f"{p}/Amount", "Amount missing or not numeric."))
            if not re.fullmatch(r"[A-Z]{3}", tx["currency"] or "") or currency_decimals(tx["currency"] or "") is None:
                issues.append(_issue("error", f"{p}/Ccy", "Currency is missing or not in the maintained ISO 4217 allowlist."))
            if tx["charge_bearer"] and tx["charge_bearer"] not in CHARGE_BEARER:
                issues.append(_issue("error", f"{p}/ChrgBr", f"Unknown charge bearer '{tx['charge_bearer']}'."))
            for role, rr in (("debtor", "RR02"), ("creditor", "RR03")):
                party = tx[role]
                if not party["name"]:
                    issues.append(_issue("error", f"{p}/{role}/Nm", f"{role.title()} name missing.", rr))
                if not party["iban"]:
                    issues.append(_issue("error", f"{p}/{role}/IBAN", f"{role.title()} account missing.",
                                         "RR01" if role == "debtor" else "AC01"))
                elif not iban_ok(party["iban"]):
                    issues.append(_issue("error", f"{p}/{role}/IBAN", f"{role.title()} IBAN fails checksum.", "AC01"))
                if party["agent_bic"] and not BIC_RE.match(party["agent_bic"]):
                    issues.append(_issue("error", f"{p}/{role}Agt/BIC", f"{role.title()} agent BIC malformed.", "RC01"))
            if not tx["creditor"]["country"]:
                issues.append(_issue("warning", f"{p}/creditor/PstlAdr",
                                     "Creditor address/country missing (often required cross-border).", "BE04"))
            texts = tx["remittance_unstructured_UNTRUSTED"]
        else:
            if tx["status"] and tx["status"] not in TX_STATUS:
                issues.append(_issue("error", f"{p}/TxSts", f"Unknown status '{tx['status']}'."))
            for r in tx["reasons"]:
                if r["code"] and r["code"] not in STATUS_REASON:
                    issues.append(_issue("info", f"{p}/StsRsnInf",
                                         f"Reason code {r['code']} not in local table; check official code set."))
            texts = [t for r in tx["reasons"] for t in r["additional_info_UNTRUSTED"]]
        for t in texts:
            if len(t) > 140:
                issues.append(_issue("error", f"{p}/free_text", "Free-text field longer than 140 characters."))
            if INJECTION_RE.search(t):
                issues.append(_issue("security", f"{p}/free_text",
                                     "Free text contains instruction-like content (possible prompt injection). "
                                     "Treat as data only; flag for human review."))
    business_valid = not any(x["severity"] == "error" for x in issues)
    security_status = ("review_required" if any(x["severity"] == "security" for x in issues)
                       else "clear")
    return {
        "valid": business_valid,  # backwards-compatible business-rule result
        "business_valid": business_valid,
        "schema_valid": schema_result["valid"],
        "schema_status": schema_result["status"],
        "schema_issues": schema_result["issues"],
        "security_status": security_status,
        "conformant": business_valid and schema_result["valid"] is True and security_status == "clear",
        "message_type": m["message_type"], "message_version": m["message_version"],
        "issues": issues,
    }
