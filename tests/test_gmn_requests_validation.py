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


_TUBE_REFERENCE_DATA = {
    "eventDate": ("2024-01-01", "date"),
    "measuringPoint": {
        "measuringPointCode": "MP1",
        "monitoringTube": {"broId": "GMW000000123456", "tubeNumber": "1"},
    },
}


def test_gmn_move_request_rejects_unsupported_srcdoc():
    with pytest.raises(Exception, match="not allowed"):
        gmn_requests_module.gmn_move_request(
            "GMN_TubeReference_Nope",
            requestReference="gmn-move-001",
            broId="GMN000000000001",
            qualityRegime="IMBRO",
            correctionReason="eigenCorrectie",
            dateToBeCorrected="2024-02-01",
            srcdocdata=_TUBE_REFERENCE_DATA,
        )


def test_gmn_move_request_requires_date_to_be_corrected():
    with pytest.raises(Exception, match="dateToBeCorrected"):
        gmn_requests_module.gmn_move_request(
            "GMN_TubeReference",
            requestReference="gmn-move-002",
            broId="GMN000000000001",
            qualityRegime="IMBRO",
            correctionReason="eigenCorrectie",
            srcdocdata=_TUBE_REFERENCE_DATA,
        )


def test_gmn_move_request_generates_expected_root_and_sourcedoc():
    request = gmn_requests_module.gmn_move_request(
        "GMN_TubeReference",
        requestReference="gmn-move-003",
        broId="GMN000000000001",
        qualityRegime="IMBRO",
        correctionReason="eigenCorrectie",
        dateToBeCorrected="2024-02-01",
        srcdocdata=_TUBE_REFERENCE_DATA,
    )
    request.generate()
    root = request.requesttree.getroot()

    assert root.tag == "moveRequest"
    assert root.find("sourceDocument/GMN_TubeReference") is not None
    assert root.find("dateToBeCorrected") is not None


def test_gmn_insert_request_generates_expected_root():
    request = gmn_requests_module.gmn_insert_request(
        "GMN_TubeReference",
        requestReference="gmn-insert-001",
        broId="GMN000000000001",
        qualityRegime="IMBRO",
        correctionReason="eigenCorrectie",
        srcdocdata=_TUBE_REFERENCE_DATA,
    )
    request.generate()
    root = request.requesttree.getroot()

    assert root.tag == "insertRequest"
    assert root.find("sourceDocument/GMN_TubeReference") is not None
    assert root.find("dateToBeCorrected") is None


def test_gmn_delete_request_generates_expected_root_for_closure():
    request = gmn_requests_module.gmn_delete_request(
        "GMN_Closure",
        requestReference="gmn-delete-001",
        broId="GMN000000000001",
        qualityRegime="IMBRO",
        correctionReason="eigenCorrectie",
        srcdocdata={"endDateMonitoring": ("2024-01-01", "date")},
    )
    request.generate()
    root = request.requesttree.getroot()

    assert root.tag == "deleteRequest"
    assert root.find("sourceDocument/GMN_Closure") is not None


def test_gmn_registration_supports_tube_reference():
    request = gmn_requests_module.gmn_registration_request(
        "GMN_TubeReference",
        requestReference="gmn-reg-003",
        qualityRegime="IMBRO",
        broId="GMN000000000001",
        srcdocdata=_TUBE_REFERENCE_DATA,
    )
    request.generate()
    root = request.requesttree.getroot()

    assert root.find("sourceDocument/GMN_TubeReference") is not None

