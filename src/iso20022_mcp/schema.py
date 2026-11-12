"""Optional local XSD validator. Does not download or bundle official schemas.

Set ISO20022_XSD_DIR to a trusted directory holding exact-version files such
as pacs.008.001.08.xsd. A missing schema is *not* treated as conformance.
"""
from __future__ import annotations

import os
from pathlib import Path
from lxml import etree
from .parser import NAMESPACE_PREFIX, SUPPORTED_VERSIONS


def validate_schema(xml: str, namespace: str) -> dict:
    directory = os.environ.get("ISO20022_XSD_DIR")
    if not directory:
        return {"status": "not_configured", "valid": None, "issues": []}
    version = namespace.removeprefix(NAMESPACE_PREFIX)
    if version not in SUPPORTED_VERSIONS:
        return {"status": "error", "valid": False, "issues": ["Unsupported schema version."]}
    file = Path(directory).expanduser().resolve() / (version + ".xsd")
    if not file.is_file():
        return {"status": "unavailable", "valid": False, "issues": [f"Local XSD not found: {file.name}"]}
    parser = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False, huge_tree=False)
    try:
        xsd_doc = etree.parse(str(file), parser)
        validator = etree.XMLSchema(xsd_doc)
        document = etree.fromstring(xml.encode("utf-8"), parser)
        ok = validator.validate(document)
        return {
            "status": "valid" if ok else "invalid",
            "valid": ok,
            "issues": [] if ok else [str(e) for e in validator.error_log[:10]],
        }
    except (etree.XMLSyntaxError, etree.XMLSchemaParseError, OSError, ValueError) as exc:
        return {"status": "error", "valid": False, "issues": [str(exc)]}
