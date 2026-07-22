import pytest
from lxml import etree

from bro_exchange.broxml.gld import requests as gld_requests_module


def _stub_startregistration(*_args, **_kwargs):
    source_document = etree.Element("sourceDocument")
    etree.SubElement(source_document, "GLD_StartRegistration")
    return source_document


def _stub_addition(*_args, **_kwargs):
    source_document = etree.Element("sourceDocument")
    etree.SubElement(source_document, "GLD_Addition")
    return source_document


def test_gld_registration_omits_empty_optional_delivery_accountable_party(monkeypatch):
    monkeypatch.setattr(
        gld_requests_module,
        "gen_gld_startregistration",
        _stub_startregistration,
    )

    request = gld_requests_module.gld_registration_request(
        "GLD_StartRegistration",
        requestReference="gld-reg-001",
        qualityRegime="IMBRO",
        deliveryAccountableParty="   ",
        srcdocdata={},
    )

    request.generate()
    root = request.requesttree.getroot()

    delivery_accountable_party = root.find(
        f"{{{gld_requests_module.ns_regreq_map_gld2['brocom']}}}deliveryAccountableParty"
    )
    assert delivery_accountable_party is None


def test_gld_registration_rejects_empty_required_quality_regime():
    with pytest.raises(Exception, match="missing or empty"):
        gld_requests_module.gld_registration_request(
            "GLD_StartRegistration",
            requestReference="gld-reg-002",
            qualityRegime=" ",
            srcdocdata={},
        )


def test_gld_replace_requires_bro_id_for_addition_even_if_empty_input(monkeypatch):
    monkeypatch.setattr(gld_requests_module, "gen_gld_addition", _stub_addition)

    request = gld_requests_module.gld_replace_request(
        "GLD_Addition",
        requestReference="gld-rep-001",
        qualityRegime="IMBRO",
        correctionReason="other",
        broId="",
        srcdocdata={},
    )

    with pytest.raises(Exception, match="broId"):
        request.generate()
