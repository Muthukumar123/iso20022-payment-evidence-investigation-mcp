"""Authorization must precede all payment message reads."""
import pytest
from iso20022_mcp.adapters import PaymentInspectionService
from iso20022_mcp.generate import generate_pacs008


class Store:
    def __init__(self):
        self.calls = []
    def read_xml(self, reference):
        self.calls.append(reference)
        return generate_pacs008()


class Access:
    def may_read(self, principal, reference):
        return principal == "payment-ops" and reference == "PAY-123"


def test_authorized_read_only_inspection():
    store = Store()
    service = PaymentInspectionService(store, Access())
    result = service.inspect(principal="payment-ops", payment_reference="PAY-123")
    assert store.calls == ["PAY-123"]
    assert result["message"]["message_type"] == "pacs.008"
    assert result["validation"]["business_valid"]


def test_unauthorized_request_fails_before_data_access():
    store = Store()
    service = PaymentInspectionService(store, Access())
    with pytest.raises(PermissionError):
        service.inspect(principal="guest", payment_reference="PAY-123")
    assert store.calls == []


@pytest.mark.parametrize("ref", ["../payments", "PAY 123", "PAY/123", ""])
def test_invalid_reference_fails_before_data_access(ref):
    store = Store()
    service = PaymentInspectionService(store, Access())
    with pytest.raises(ValueError):
        service.inspect(principal="payment-ops", payment_reference=ref)
    assert store.calls == []
