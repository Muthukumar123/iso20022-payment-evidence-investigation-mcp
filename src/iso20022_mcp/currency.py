"""Curated ISO 4217 payment-currency set; review against the official standard.

This is an explicit allowlist, not the full ISO 4217 registry. Unlisted currencies
require reference-data maintenance rather than silently receiving two decimals.
"""
CURRENCIES = set("""
AED AFN ALL AMD AOA ARS AUD AWG AZN BAM BBD BDT BGN BHD BIF BMD BND BOB
BRL BSD BTN BWP BYN BZD CAD CDF CHF CLP CNY COP CRC CUP CVE CZK DJF DKK
DOP DZD EGP ERN ETB EUR FJD FKP GBP GEL GHS GIP GMD GNF GTQ GYD HKD
HNL HTG HUF IDR ILS INR IQD IRR ISK JMD JOD JPY KES KGS KHR KMF KPW
KRW KWD KYD KZT LAK LBP LKR LRD LSL LYD MAD MDL MGA MKD MMK MNT MOP
MRU MUR MVR MWK MXN MYR MZN NAD NGN NIO NOK NPR NZD OMR PAB PEN PGK
PHP PKR PLN PYG QAR RON RSD RUB RWF SAR SBD SCR SDG SEK SGD SHP SLE
SOS SRD SSP STN SVC SYP SZL THB TJS TMT TND TOP TRY TTD TWD TZS UAH
UGX USD UYU UZS VES VND VUV WST XAF XCD XOF XPF YER ZAR ZMW
""".split())
ZERO_DECIMAL = set("BIF CLP DJF GNF ISK JPY KMF KRW PYG RWF UGX VND VUV XAF XOF XPF".split())
THREE_DECIMAL = set("BHD IQD JOD KWD LYD OMR TND".split())


def currency_decimals(code: str) -> int | None:
    """Return supported currency minor units, or None for unrecognized codes."""
    if code not in CURRENCIES:
        return None
    if code in ZERO_DECIMAL:
        return 0
    if code in THREE_DECIMAL:
        return 3
    return 2
