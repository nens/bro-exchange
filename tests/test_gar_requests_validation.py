import pytest
from lxml import etree

from bro_exchange.broxml.gar import requests as gar_requests_module

FIELD_RESEARCH = {
    "samplingDateTime": "2024-01-01T10:00:00+01:00",
    "samplingStandard": "onbekend",
    "pumpType": "onbekend",
    "abnormalityInCooling": "nee",
    "abnormalityInDevice": "nee",
    "pollutedByEngine": "nee",
    "filterAerated": "nee",
    "groundWaterLevelDroppedTooMuch": "nee",
    "abnormalFilter": "nee",
    "sampleAerated": "nee",
    "hoseReused": "nee",
    "temperatureDifficultToMeasure": "nee",
}

GAR_DATA = {
    "objectIdAccountableParty": "obj-001",
    "qualityControlMethod": "onbekend",
    "gmwBroId": "GMW000000123456",
    "tubeNumber": "1",
    "fieldResearch": FIELD_RESEARCH,
}


def test_gar_registration_rejects_unsupported_srcdoc():
    with pytest.raises(Exception, match="not allowed"):
        gar_requests_module.gar_registration_request(
            "GAR_Nope",
            requestReference="gar-ref-001",
            qualityRegime="IMBRO",
            srcdocdata=GAR_DATA,
        )


def test_gar_registration_requires_field_research():
    request = gar_requests_module.gar_registration_request(
        "GAR",
        requestReference="gar-ref-002",
        qualityRegime="IMBRO",
        srcdocdata={
            "objectIdAccountableParty": "obj-001",
            "qualityControlMethod": "onbekend",
            "gmwBroId": "GMW000000123456",
            "tubeNumber": "1",
        },
    )
    with pytest.raises(Exception, match="fieldResearch"):
        request.generate()


def test_gar_registration_generates_expected_root_and_sourcedoc():
    request = gar_requests_module.gar_registration_request(
        "GAR",
        requestReference="gar-ref-003",
        qualityRegime="IMBRO",
        srcdocdata=GAR_DATA,
    )
    request.generate()
    root = request.requesttree.getroot()

    assert root.tag == "registrationRequest"
    assert root.find("sourceDocument/GAR") is not None
    assert root.find("sourceDocument/GAR/monitoringPoint") is not None


def test_gar_replace_requires_correction_reason():
    with pytest.raises(Exception, match="missing or empty"):
        gar_requests_module.gar_replace_request(
            "GAR",
            requestReference="gar-ref-004",
            broId="GAR000000000001",
            qualityRegime="IMBRO",
            correctionReason="",
            srcdocdata=GAR_DATA,
        )


def test_gar_replace_generates_correction_request_root():
    request = gar_requests_module.gar_replace_request(
        "GAR",
        requestReference="gar-ref-005",
        broId="GAR000000000001",
        qualityRegime="IMBRO",
        correctionReason="eigenCorrectie",
        srcdocdata=GAR_DATA,
    )
    request.generate()
    root = request.requesttree.getroot()

    assert root.tag == "correctionRequest"
    assert root.find("sourceDocument/GAR") is not None
    correction_reason = root.find("correctionReason")
    assert correction_reason is not None
    assert correction_reason.get("codeSpace") == "urn:bro:gar:CorrectionReason"


def test_gar_registration_includes_laboratory_analyses_and_field_measurements():
    data = dict(GAR_DATA)
    data["fieldResearch"] = dict(
        FIELD_RESEARCH,
        fieldMeasurements=[
            {
                "parameter": "pH",
                "unit": "1",
                "fieldMeasurementValue": 7.1,
                "qualityControlStatus": "onbekend",
            }
        ],
    )
    data["laboratoryAnalyses"] = [
        {
            "responsibleLaboratoryKvk": "12345678",
            "analysisProcesses": [
                {
                    "date": "2024-01-05",
                    "analyticalTechnique": "onbekend",
                    "valuationMethod": "onbekend",
                    "analyses": [
                        {
                            "parameter": "Cl",
                            "unit": "mg/l",
                            "analysisMeasurementValue": 12.3,
                            "qualityControlStatus": "onbekend",
                        }
                    ],
                }
            ],
        }
    ]

    request = gar_requests_module.gar_registration_request(
        "GAR",
        requestReference="gar-ref-006",
        qualityRegime="IMBRO",
        srcdocdata=data,
    )
    request.generate()
    root = request.requesttree.getroot()

    garcom = "http://www.broservices.nl/xsd/garcommon/1.0"
    assert root.find(f"sourceDocument/GAR/fieldResearch/{{{garcom}}}fieldMeasurement") is not None
    assert root.find("sourceDocument/GAR/laboratoryAnalysis") is not None
    assert root.find(f"sourceDocument/GAR/laboratoryAnalysis/{{{garcom}}}analysisProcess/{{{garcom}}}analysis") is not None
