import pytest
from lxml import etree

from bro_exchange.broxml.gmw import requests as gmw_requests_module


def _stub_source_document(*_args, **_kwargs):
    source_document = etree.Element("sourceDocument")
    etree.SubElement(source_document, "dummy")
    return source_document


def test_gmw_registration_does_not_auto_set_under_privilege(monkeypatch):
    monkeypatch.setattr(
        gmw_requests_module,
        "gen_gmw_construction",
        _stub_source_document,
    )

    request = gmw_requests_module.gmw_registration_request(
        "GMW_Construction",
        requestReference="req-001",
        qualityRegime="IMBRO",
        srcdocdata={},
    )

    request.generate()
    root = request.requesttree.getroot()

    under_privilege = root.find(
        f"{{{gmw_requests_module.ns_regreq_map_gmw1['ns1']}}}underPrivilege"
    )
    assert under_privilege is None


def test_gmw_registration_adds_under_privilege_when_provided(monkeypatch):
    monkeypatch.setattr(
        gmw_requests_module,
        "gen_gmw_construction",
        _stub_source_document,
    )

    request = gmw_requests_module.gmw_registration_request(
        "GMW_Construction",
        requestReference="req-002",
        qualityRegime="IMBRO",
        underPrivilege="ja",
        srcdocdata={},
    )

    request.generate()
    root = request.requesttree.getroot()

    under_privilege = root.find(
        f"{{{gmw_requests_module.ns_regreq_map_gmw1['ns1']}}}underPrivilege"
    )
    assert under_privilege is not None
    assert under_privilege.text == "ja"


def test_gmw_registration_owner_requires_non_empty_bro_id():
    request = gmw_requests_module.gmw_registration_request(
        "GMW_Owner",
        requestReference="req-003",
        qualityRegime="IMBRO",
        broId=None,
        srcdocdata={},
    )

    with pytest.raises(Exception, match="broId"):
        request.generate()


def test_gmw_replace_requires_non_empty_required_fields():
    with pytest.raises(Exception, match="missing or empty"):
        gmw_requests_module.gmw_replace_request(
            "GMW_Owner",
            requestReference="req-004",
            broId=None,
            qualityRegime="IMBRO",
            correctionReason="other",
            srcdocdata={},
        )


def test_gmw_move_requires_non_empty_date_to_be_corrected():
    with pytest.raises(Exception, match="missing or empty"):
        gmw_requests_module.gmw_move_request(
            "GMW_Owner",
            requestReference="req-005",
            broId="GMW000000001",
            qualityRegime="IMBRO",
            correctionReason="other",
            dateToBeCorrected=" ",
            srcdocdata={},
        )


def test_gmw_replace_omits_empty_delivery_accountable_party(monkeypatch):
    monkeypatch.setattr(
        gmw_requests_module,
        "gen_gmw_owner",
        _stub_source_document,
    )

    request = gmw_requests_module.gmw_replace_request(
        "GMW_Owner",
        requestReference="req-006",
        deliveryAccountableParty="   ",
        broId="GMW000000002",
        qualityRegime="IMBRO",
        correctionReason="other",
        srcdocdata={},
    )

    request.generate()
    root = request.requesttree.getroot()

    delivery_accountable_party = root.find(
        f"{{{gmw_requests_module.ns_regreq_map_gmw1['ns1']}}}deliveryAccountableParty"
    )
    assert delivery_accountable_party is None
