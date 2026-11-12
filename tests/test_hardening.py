"""Regression tests for bounded parsing, schema outcomes, and security isolation."""
import pytest
from iso20022_mcp import generate, parser, validate
from iso20022_mcp.currency import currency_decimals
from iso20022_mcp import server


def test_version_is_extracted():
    message = parser.parse_message(generate.generate_pacs008())
    assert message["message_version"] == "pacs.008.001.08"


def test_unsupported_version_rejected():
    xml = generate.generate_pacs008().replace("pacs.008.001.08", "pacs.008.001.99")
    with pytest.raises(parser.ParseError, match="Unsupported"):
        parser.parse_message(xml)


def test_wrong_message_root_rejected():
    xml = generate.generate_pacs008().replace("FIToFICstmrCdtTrf", "FIToFIPmtStsRpt")
    with pytest.raises(parser.ParseError, match="requires message root"):
        parser.parse_message(xml)


def test_non_iso_namespace_rejected():
    xml = generate.generate_pacs008().replace(
        "urn:iso:std:iso:20022:tech:xsd:", "urn:untrusted:"
    )
    with pytest.raises(parser.ParseError, match="ISO 20022 namespace"):
        parser.parse_message(xml)


def test_oversized_xml_rejected():
    result = validate.validate_message(" " * (parser.MAX_XML_BYTES + 1))
    assert not result["valid"]
    assert "maximum size" in result["issues"][0]["message"]


def test_doctype_rejected():
    xml = generate.generate_pacs008().replace(
        "<Document ", "<!DOCTYPE Document [<!ENTITY e 'hello'>]>\n<Document "
    )
    with pytest.raises(parser.ParseError, match="DOCTYPE"):
        parser.parse_message(xml)


def test_mismatched_nested_namespace_rejected():
    xml = generate.generate_pacs008().replace(
        "<Dbtr><Nm>", '<Dbtr xmlns="urn:foreign"><Nm>'
    )
    with pytest.raises(parser.ParseError, match="namespaces"):
        parser.parse_message(xml)


def test_unrecognized_currency_is_error():
    result = validate.validate_message(generate.generate_pacs008(currency="ZZZ"))
    assert not result["business_valid"]
    assert any(i["field"].endswith("/Ccy") for i in result["issues"])
    assert currency_decimals("ZZZ") is None


@pytest.mark.parametrize("amount", ["NaN", "Infinity", "-Infinity", "0"])
def test_invalid_amount_rejected(amount):
    result = validate.validate_message(generate.generate_pacs008(amount=amount))
    assert not result["business_valid"]


def test_missing_transaction_count_rejected():
    xml = generate.generate_pacs008().replace("<NbOfTxs>1</NbOfTxs>", "")
    assert not validate.validate_message(xml)["business_valid"]


def test_iban_country_length_checked():
    assert validate.iban_ok("NL91ABNA0417164300")
    assert not validate.iban_ok("NL91ABNA04171643000")


def test_security_result_is_distinct(monkeypatch):
    monkeypatch.delenv("ISO20022_XSD_DIR", raising=False)
    result = validate.validate_message(generate.generate_pacs008("injection_in_remittance"))
    assert result["business_valid"]
    assert result["security_status"] == "review_required"
    assert result["schema_status"] == "not_configured"
    assert result["schema_valid"] is None
    assert result["conformant"] is False


def test_missing_xsd_is_not_conformant(monkeypatch, tmp_path):
    monkeypatch.setenv("ISO20022_XSD_DIR", str(tmp_path))
    result = validate.validate_message(generate.generate_pacs008())
    assert result["business_valid"]
    assert result["schema_status"] == "unavailable"
    assert result["schema_valid"] is False
    assert not result["conformant"]


def test_xsd_engine_uses_local_file(monkeypatch, tmp_path):
    # This intentionally permissive XSD tests wiring only, not ISO conformance.
    xsd = """<?xml version="1.0"?>
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
      targetNamespace="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08"
      elementFormDefault="qualified">
      <xs:element name="Document"><xs:complexType><xs:sequence>
        <xs:any minOccurs="1" maxOccurs="1" processContents="skip"/>
      </xs:sequence></xs:complexType></xs:element>
    </xs:schema>"""
    (tmp_path / "pacs.008.001.08.xsd").write_text(xsd, encoding="utf-8")
    monkeypatch.setenv("ISO20022_XSD_DIR", str(tmp_path))
    result = validate.validate_message(generate.generate_pacs008())
    assert result["schema_status"] == "valid"
    assert result["schema_valid"] is True
    assert result["conformant"] is True


def test_mcp_handlers_return_dicts():
    assert isinstance(server.lookup_code("AC04"), dict)
    assert isinstance(server.parse_message(generate.generate_pacs008()), dict)
    assert isinstance(server.validate_message(generate.generate_pacs008()), dict)


def test_generator_rejects_unsupported_kind():
    assert server.generate_test_message(kind="camt.053").startswith("Error:")
    assert server.generate_test_message(defect="unknown").startswith("Error:")
