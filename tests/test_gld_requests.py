from lxml import etree

from bro_exchange.broxml.gld import requests as gld_requests_module


def _stub_source_document(*_args, **_kwargs):
    source_document = etree.Element("sourceDocument")
    etree.SubElement(source_document, "GLD_StartRegistration")
    return source_document


def test_gld_replace_delivery_accountable_party_is_written(monkeypatch):
    monkeypatch.setattr(
        gld_requests_module,
        "gen_gld_startregistration",
        _stub_source_document,
    )

    request = gld_requests_module.gld_replace_request(
        "GLD_StartRegistration",
        requestReference="ref-001",
        qualityRegime="IMBRO",
        correctionReason="other",
        broId="GLD000000001",
        deliveryAccountableParty=12345678,
        srcdocdata={},
    )

    request.generate()
    root = request.requesttree.getroot()

    delivery_accountable_party = root.find(
        f"{{{gld_requests_module.ns_regreq_map_gld2['brocom']}}}deliveryAccountableParty"
    )

    assert delivery_accountable_party is not None
    assert delivery_accountable_party.text == "12345678"


def test_gld_replace_omits_delivery_accountable_party_if_not_provided(monkeypatch):
    monkeypatch.setattr(
        gld_requests_module,
        "gen_gld_startregistration",
        _stub_source_document,
    )

    request = gld_requests_module.gld_replace_request(
        "GLD_StartRegistration",
        requestReference="ref-002",
        qualityRegime="IMBRO",
        correctionReason="other",
        broId="GLD000000002",
        srcdocdata={},
    )

    request.generate()
    root = request.requesttree.getroot()

    delivery_accountable_party = root.find(
        f"{{{gld_requests_module.ns_regreq_map_gld2['brocom']}}}deliveryAccountableParty"
    )

    assert delivery_accountable_party is None


def test_gld_delete_accepts_closure_and_parses_request_reference():
    srcdoc = b"""
        <registrationRequest xmlns:brocom=\"http://www.broservices.nl/xsd/brocommon/3.0\">
            <brocom:requestReference>ref-delete-001</brocom:requestReference>
            <brocom:qualityRegime>IMBRO</brocom:qualityRegime>
            <sourceDocument>
                <GLD_Closure />
            </sourceDocument>
        </registrationRequest>
    """

    request = gld_requests_module.gld_delete_request(
        srcdoc=srcdoc,
        correctionReason="other",
    )

    request.generate()
    root = request.requesttree.getroot()

    assert root.tag == "deleteRequest"
    assert request.requestreference == "ref-delete-001"

    correction_reason_elements = [
        element for element in root.iter() if "correctionReason" in element.tag
    ]
    assert len(correction_reason_elements) == 1
    assert correction_reason_elements[0].text == "other"
