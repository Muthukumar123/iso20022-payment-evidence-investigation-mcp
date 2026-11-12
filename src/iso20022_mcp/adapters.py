"""Read-only, fail-closed payment-hub integration contract.

Transport and identity infrastructure are intentionally injected by the
deploying bank. This module neither connects to a payment hub nor writes
payments; it provides an authorization boundary before reading XML.
"""
from __future__ import annotations

import re
from typing import Protocol

from .parser import parse_message
from .validate import validate_message

PAYMENT_REFERENCE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")


class PaymentMessageSource(Protocol):
    """Bank-owned read-only adapter to a payment hub or message archive."""

    def read_xml(self, payment_reference: str) -> str | None:
        ...


class PaymentReadAuthorizer(Protocol):
    """Bank-owned policy enforcement using the authenticated principal."""

    def may_read(self, principal: str, payment_reference: str) -> bool:
        ...


class PaymentInspectionService:
    """No payment mutation methods; deny access unless a policy permits it."""

    def __init__(self, source: PaymentMessageSource, authorizer: PaymentReadAuthorizer):
        self._source = source
        self._authorizer = authorizer

    def inspect(self, *, principal: str, payment_reference: str) -> dict:
        if not principal or not PAYMENT_REFERENCE.fullmatch(payment_reference):
            raise ValueError("Authenticated principal and valid payment reference required.")
        if not self._authorizer.may_read(principal, payment_reference):
            raise PermissionError("Payment message access denied.")
        xml = self._source.read_xml(payment_reference)
        if xml is None:
            raise LookupError("Payment message not found.")
        return {
            "payment_reference": payment_reference,
            "message": parse_message(xml),
            "validation": validate_message(xml),
        }
