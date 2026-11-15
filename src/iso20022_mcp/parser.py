"""Bounded, namespace- and version-aware ISO 20022 XML parsing."""
from __future__ import annotations

from lxml import etree

SUPPORTED_VERSIONS = {
    "pacs.008.001.08": ("pacs.008", "FIToFICstmrCdtTrf"),
    "pacs.002.001.10": ("pacs.002", "FIToFIPmtStsRpt"),
}
NAMESPACE_PREFIX = "urn:iso:std:iso:20022:tech:xsd:"
MAX_XML_BYTES = 1_000_000
MAX_XML_ELEMENTS = 10_000


class ParseError(ValueError):
    """Invalid, unsupported, or unsafe ISO 20022 XML."""


def _ln(el) -> str:
    return etree.QName(el).localname


def _children(el, name: str):
    if el is None:
        return []
    return [c for c in el if isinstance(c.tag, str) and _ln(c) == name]


def _find(el, path: str):
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
    """Return (business root, message family, namespace) after basic safety checks."""
    if not isinstance(xml, str):
        raise ParseError("XML input must be a string.")
    try:
        raw = xml.encode("utf-8")
    except UnicodeError as exc:
        raise ParseError("XML contains invalid Unicode.") from exc
    if len(raw) > MAX_XML_BYTES:
        raise ParseError(f"XML exceeds maximum size of {MAX_XML_BYTES} bytes.")
    try:
        parser = etree.XMLParser(
            resolve_entities=False, no_network=True, load_dtd=False, huge_tree=False,
            remove_comments=True, remove_pis=True,
        )
        root = etree.fromstring(raw, parser)
        if root.getroottree().docinfo.doctype:
            raise ParseError("DOCTYPE and entity declarations are not permitted.")
    except etree.XMLSyntaxError as exc:
        raise ParseError(f"Not well-formed XML: {exc}") from exc
    if root is None:
        raise ParseError("Empty XML document.")
    ns = etree.QName(root).namespace or ""
    if not ns.startswith(NAMESPACE_PREFIX):
        raise ParseError("Document must declare a supported ISO 20022 namespace.")
    version = ns[len(NAMESPACE_PREFIX):]
    if version not in SUPPORTED_VERSIONS:
        raise ParseError(f"Unsupported ISO 20022 message version '{version}'.")
    kind, expected_root = SUPPORTED_VERSIONS[version]
    if _ln(root) == "Document":
        children = [c for c in root if isinstance(c.tag, str)]
        if len(children) != 1:
            raise ParseError("Document must contain exactly one business-message element.")
        body = children[0]
    else:
        body = root
    if _ln(body) != expected_root:
        raise ParseError(f"Namespace {version} requires message root '{expected_root}'.")
    count = 0
    for element in root.iter():
        if not isinstance(element.tag, str):
            continue
        count += 1
        if count > MAX_XML_ELEMENTS:
            raise ParseError(f"XML exceeds maximum element count of {MAX_XML_ELEMENTS}.")
        if etree.QName(element).namespace != ns:
            raise ParseError("Mixed or missing element namespaces are not supported.")
    return body, kind, ns


def _party(tx, role: str) -> dict:
    return {
        "name": _text(tx, f"{role}/Nm"),
        "country": _text(tx, f"{role}/PstlAdr/Ctry"),
        "iban": _text(tx, f"{role}Acct/Id/IBAN"),
        "agent_bic": _text(tx, f"{role}Agt/FinInstnId/BICFI"),
    }


def parse_message(xml: str) -> dict:
    body, kind, ns = _load(xml)
    out = {
        "message_type": kind,
        "message_version": ns[len(NAMESPACE_PREFIX):],
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
                "remittance_unstructured_UNTRUSTED": [
                    u.text or "" for u in _children(_find(tx, "RmtInf"), "Ustrd")
                ],
            })
    else:
        out["original_msg_id"] = _text(body, "OrgnlGrpInfAndSts/OrgnlMsgId")
        out["original_msg_type"] = _text(body, "OrgnlGrpInfAndSts/OrgnlMsgNmId")
        out["group_status"] = _text(body, "OrgnlGrpInfAndSts/GrpSts")
        for tx in _children(body, "TxInfAndSts"):
            reasons = [{
                "code": _text(sri, "Rsn/Cd"),
                "additional_info_UNTRUSTED": [
                    a.text or "" for a in _children(sri, "AddtlInf")
                ],
            } for sri in _children(tx, "StsRsnInf")]
            out["transactions"].append({
                "original_end_to_end_id": _text(tx, "OrgnlEndToEndId"),
                "original_uetr": _text(tx, "OrgnlUETR"),
                "status": _text(tx, "TxSts"),
                "reasons": reasons,
            })
    out["actual_tx_count"] = len(out["transactions"])
    return out
