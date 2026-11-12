import pytest
from iso20022_mcp import parser, validate, explain, codes, generate


def test_valid_message_passes():
    r = validate.validate_message(generate.generate_pacs008())
    assert r["valid"], r["issues"]


@pytest.mark.parametrize("defect,code", [
    ("bad_iban", "AC01"), ("bad_bic", "RC01"), ("missing_creditor_name", "RR03"),
    ("missing_creditor_address", "BE04")])
def test_defects_map_to_reject_codes(defect, code):
    r = validate.validate_message(generate.generate_pacs008(defect))
    assert code in {i.get("likely_reject_code") for i in r["issues"]}


@pytest.mark.parametrize("defect", ["bad_decimals", "count_mismatch"])
def test_structural_defects_invalid(defect):
    assert not validate.validate_message(generate.generate_pacs008(defect))["valid"]


def test_injection_flagged():
    r = validate.validate_message(generate.generate_pacs008("injection_in_remittance"))
    assert any(i["severity"] == "security" for i in r["issues"])


def test_pacs002_explain():
    text = explain.explain_message(generate.generate_pacs002("AC04"))
    assert "RJCT" in text and "Closed account" in text


def test_unknown_code_not_guessed():
    assert codes.lookup_code("ZZ99")["found"] is False


def test_malformed_xml():
    r = validate.validate_message("<Document><broken>")
    assert not r["valid"] and r["issues"][0]["likely_reject_code"] == "FF01"


def test_xxe_not_resolved():
    xml = ('<?xml version="1.0"?><!DOCTYPE d [<!ENTITY x SYSTEM "file:///etc/passwd">]>'
           '<Document><FIToFICstmrCdtTrf><GrpHdr><MsgId>&x;</MsgId></GrpHdr></FIToFICstmrCdtTrf></Document>')
    try:
        m = parser.parse_message(xml)
        assert "root:" not in (m["msg_id"] or "")
    except parser.ParseError:
        pass  # rejecting the document is also safe


def test_iban_checksum():
    assert validate.iban_ok("NL91ABNA0417164300")
    assert not validate.iban_ok("NL91ABNA0417164301")
