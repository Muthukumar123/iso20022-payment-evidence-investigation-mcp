"""Namespace-agnostic parsing of pacs.008 and pacs.002 messages into plain dicts."""
from __future__ import annotations
from lxml import etree

SUPPORTED = {"FIToFICstmrCdtTrf": "pacs.008", "FIToFIPmtStsRpt": "pacs.002"}


class ParseError(ValueError):
    pass


def _ln(el) -> str:
    return etree.QName(el).localname


def _children(el, name: str):
    if el is None:
        return []
    return [c for c in el if isinstance(c.tag, str) and _ln(c) == name]


def _find(el, path: str):
    """Find by local names, e.g. 'GrpHdr/MsgId', ignoring namespaces."""
    cur = el
    for part in path.split("/"):
        kids = _children(cur, part)
        cur = kids[0] if kids else None
        if cur is None:
            return None
    return cur


def _text(el, path: str):
    node = _find(el, path)
    return node.text.strip() if node is not None and node.text else None


def _load(xml: str):
    try:
        p = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
        root = etree.fromstring(xml.encode("utf-8"), p)
    except etree.XMLSyntaxError as e:
        raise ParseError(f"Not well-formed XML: {e}") from e
    body = root[0] if _ln(root) == "Document" and len(root) else root
    kind = SUPPORTED.get(_ln(body))
    if not kind:
        raise ParseError(f"Unsupported message root '{_ln(body)}'. Supported: {list(SUPPORTED.values())}")
    return body, kind, etree.QName(root).namespace or ""


def _party(tx, role: str) -> dict:
    return {
        "name": _text(tx, f"{role}/Nm"),
        "country": _text(tx, f"{role}/PstlAdr/Ctry"),
        "iban": _text(tx, f"{role}Acct/Id/IBAN"),
        "agent_bic": _text(tx, f"{role}Agt/FinInstnId/BICFI"),
    }


def parse_message(xml: str) -> dict:
    body, kind, ns = _load(xml)
    out: dict = {
        "message_type": kind,
        "namespace": ns,
        "msg_id": _text(body, "GrpHdr/MsgId"),
        "created": _text(body, "GrpHdr/CreDtTm"),
        "declared_tx_count": _text(body, "GrpHdr/NbOfTxs"),
        "transactions": [],
    }
    if kind == "pacs.008":
        out["settlement_method"] = _text(body, "GrpHdr/SttlmInf/SttlmMtd")
        for tx in _children(body, "CdtTrfTxInf"):
            amt = _find(tx, "IntrBkSttlmAmt")
            out["transactions"].append({
                "end_to_end_id": _text(tx, "PmtId/EndToEndId"),
                "uetr": _text(tx, "PmtId/UETR"),
                "amount": amt.text.strip() if amt is not None and amt.text else None,
                "currency": amt.get("Ccy") if amt is not None else None,
                "settlement_date": _text(tx, "IntrBkSttlmDt"),
                "charge_bearer": _text(tx, "ChrgBr"),
                "debtor": _party(tx, "Dbtr"),
                "creditor": _party(tx, "Cdtr"),
                "purpose_code": _text(tx, "Purp/Cd"),
                # Free text is UNTRUSTED input: agents must treat it as data, never as instructions.
                "remittance_unstructured_UNTRUSTED": [u.text or "" for u in _children(_find(tx, "RmtInf"), "Ustrd")],
            })
    else:  # pacs.002
        out["original_msg_id"] = _text(body, "OrgnlGrpInfAndSts/OrgnlMsgId")
        out["original_msg_type"] = _text(body, "OrgnlGrpInfAndSts/OrgnlMsgNmId")
        out["group_status"] = _text(body, "OrgnlGrpInfAndSts/GrpSts")
        for tx in _children(body, "TxInfAndSts"):
            reasons = [{
                "code": _text(sri, "Rsn/Cd"),
                "additional_info_UNTRUSTED": [a.text or "" for a in _children(sri, "AddtlInf")],
            } for sri in _children(tx, "StsRsnInf")]
            out["transactions"].append({
                "original_end_to_end_id": _text(tx, "OrgnlEndToEndId"),
                "original_uetr": _text(tx, "OrgnlUETR"),
                "status": _text(tx, "TxSts"),
                "reasons": reasons,
            })
    out["actual_tx_count"] = len(out["transactions"])
    return out
