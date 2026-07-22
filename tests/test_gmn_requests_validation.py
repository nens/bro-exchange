import pytest
from lxml import etree

from bro_exchange.broxml.gmn import requests as gmn_requests_module


def _stub_startregistration(*_args, **_kwargs):
    source_document = etree.Element("sourceDocument")
    etree.SubElement(source_document, "GMN_StartRegistration")
    return source_document


def _stub_measuringpoint(*_args, **_kwargs):
    source_document = etree.Element("sourceDocument")
    etree.SubElement(source_document, "GMN_MeasuringPoint")
    return source_document


def test_gmn_registration_omits_empty_optional_delivery_accountable_party(monkeypatch):
    monkeypatch.setattr(
        gmn_requests_module,
        "gen_gmn_startregistartion",
        _stub_startregistration,
    )

    request = gmn_requests_module.gmn_registration_request(
        "GMN_StartRegistration",
        requestReference="gmn-reg-001",
        qualityRegime="IMBRO",
        deliveryAccountableParty="  ",
        srcdocdata={},
    )

    request.generate()
    root = request.requesttree.getroot()

    delivery_accountable_party = root.find(
        f"{{{gmn_requests_module.ns_regreq_map_gmn2['brocom']}}}deliveryAccountableParty"
    )
    assert delivery_accountable_party is None


def test_gmn_registration_requires_bro_id_for_measuring_point(monkeypatch):
    monkeypatch.setattr(
        gmn_requests_module,
        "gen_gmn_measuringpoint",
        _stub_measuringpoint,
    )

    request = gmn_requests_module.gmn_registration_request(
        "GMN_MeasuringPoint",
        requestReference="gmn-reg-002",
        qualityRegime="IMBRO",
        broId="",
        srcdocdata={},
    )

    with pytest.raises(Exception, match="broId"):
        request.generate()


def test_gmn_replace_rejects_empty_required_bro_id():
    with pytest.raises(Exception, match="missing or empty"):
        gmn_requests_module.gmn_replace_request(
            "GMN_MeasuringPoint",
            requestReference="gmn-rep-001",
            broId="  ",
            qualityRegime="IMBRO",
            correctionReason="other",
            srcdocdata={},
        )
