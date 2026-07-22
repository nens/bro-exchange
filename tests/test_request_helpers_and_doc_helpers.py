from dataclasses import dataclass

from lxml import etree

from bro_exchange.broxml.gld import requests as gld_requests_module
from bro_exchange.broxml.gmn import requests as gmn_requests_module
from bro_exchange.broxml.gmw import requests as gmw_requests_module
from bro_exchange.broxml.request_helpers import SourceDocData


@dataclass
class StubPayload:
    key: str
    count: int


def _stub_source_document(*_args, **_kwargs):
    source_document = etree.Element("sourceDocument")
    etree.SubElement(source_document, "dummy")
    return source_document


def test_gld_accepts_dataclass_srcdocdata(monkeypatch):
    monkeypatch.setattr(
        gld_requests_module,
        "gen_gld_startregistration",
        _stub_source_document,
    )

    request = gld_requests_module.gld_registration_request(
        "GLD_StartRegistration",
        requestReference="gld-dc-001",
        qualityRegime="IMBRO",
        srcdocdata=StubPayload(key="alpha", count=1),
    )

    request.generate()
    assert request.requesttree.getroot().tag == "registrationRequest"


def test_gmn_accepts_sourcedocdata_wrapper(monkeypatch):
    monkeypatch.setattr(
        gmn_requests_module,
        "gen_gmn_startregistartion",
        _stub_source_document,
    )

    request = gmn_requests_module.gmn_registration_request(
        "GMN_StartRegistration",
        requestReference="gmn-dc-001",
        qualityRegime="IMBRO",
        srcdocdata=SourceDocData(data={"key": "beta", "count": 2}),
    )

    request.generate()
    assert request.requesttree.getroot().tag == "registrationRequest"


def test_gmw_accepts_dataclass_srcdocdata(monkeypatch):
    monkeypatch.setattr(
        gmw_requests_module,
        "gen_gmw_construction",
        _stub_source_document,
    )

    request = gmw_requests_module.gmw_registration_request(
        "GMW_Construction",
        requestReference="gmw-dc-001",
        qualityRegime="IMBRO",
        srcdocdata=StubPayload(key="gamma", count=3),
    )

    request.generate()
    assert request.requesttree.getroot().tag.endswith("registrationRequest")


def test_supported_srcdoc_helpers_return_expected_keys():
    assert set(gld_requests_module.get_supported_gld_srcdocs().keys()) == {
        "registration",
        "replace",
        "delete",
    }
    assert set(gmn_requests_module.get_supported_gmn_srcdocs().keys()) == {
        "registration",
        "replace",
    }
    assert set(gmw_requests_module.get_supported_gmw_srcdocs().keys()) == {
        "registration",
        "replace",
        "move",
        "delete",
        "insert",
    }
