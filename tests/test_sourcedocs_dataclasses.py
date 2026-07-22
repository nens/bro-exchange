from lxml import etree

from bro_exchange.broxml.data_models import (
    GldMonitoringPointRef,
    GldStartRegistrationData,
    GmnMeasuringPoint,
    GmnMonitoringTubeRef,
    GmnStartRegistrationData,
    GmwConstructionRegistrationData,
    GmwDeliveredLocation,
    GmwDeliveredVerticalPosition,
)
from bro_exchange.broxml.gld.sourcedocs import gen_gld_startregistration
from bro_exchange.broxml.gmn.sourcedocs import gen_gmn_startregistartion
from bro_exchange.broxml.gmw.sourcedocs import gen_gmw_construction
from bro_exchange.broxml.mappings import (
    codespace_map_gld1,
    codespace_map_gmw1,
    ns_regreq_map_gld2,
    ns_regreq_map_gmw1,
)


def test_gmw_construction_accepts_dataclasses_through_constructables():
    payload = GmwConstructionRegistrationData(
        objectIdAccountableParty="obj-001",
        deliveryContext="aanlevering",
        constructionStandard="NEN",
        initialFunction="monitoring",
        numberOfMonitoringTubes=1,
        groundLevelStable="ja",
        owner=12345678,
        wellHeadProtector="geen",
        wellConstructionDate="2024-01-01",
        deliveredLocation=GmwDeliveredLocation(
            X=120000.0,
            Y=480000.0,
            horizontalPositioningMethod="ingemeten",
        ),
        deliveredVerticalPosition=GmwDeliveredVerticalPosition(
            localVerticalReferencePoint="maaiveld",
            offset=0.0,
            verticalDatum="NAP",
            groundLevelPosition=1.2,
            groundLevelPositioningMethod="ingemeten",
        ),
        monitoringTubes=[
            {
                "tubeNumber": 1,
                "tubeType": "peilbuis",
                "artesianWellCapPresent": "nee",
                "sedimentSumpPresent": "nee",
                "numberOfGeoOhmCables": 0,
                "tubeTopDiameter": 63,
                "variableDiameter": "nee",
                "tubeStatus": "inGebruik",
                "tubeTopPosition": 0.5,
                "tubeTopPositioningMethod": "ingemeten",
                "materialUsed": {
                    "tubePackingMaterial": "zand",
                    "tubeMaterial": "pvc",
                    "glue": "geen",
                },
                "screen": {
                    "screenLength": 2.0,
                    "sockMaterial": "geen",
                },
                "plainTubePart": {
                    "plainTubePartLength": 1.0,
                },
            }
        ],
    )

    source_document = gen_gmw_construction(
        payload,
        ns_regreq_map_gmw1,
        codespace_map_gmw1,
        "GMW_Construction",
    )

    assert source_document.tag.endswith("sourceDocument")
    monitoring_tube_nodes = list(source_document.iter())
    assert any(node.tag.endswith("monitoringTube") for node in monitoring_tube_nodes)


def test_gmn_startregistration_accepts_nested_dataclasses():
    payload = GmnStartRegistrationData(
        objectIdAccountableParty="obj-002",
        name="Meetnet A",
        deliveryContext="aanlevering",
        monitoringPurpose="monitoring",
        groundwaterAspect="kwantiteit",
        startDateMonitoring=["2024-01-01", "date"],
        measuringPoints=[
            GmnMeasuringPoint(
                measuringPointCode="MP-001",
                monitoringTube=GmnMonitoringTubeRef(
                    broId="GMW000000001",
                    tubeNumber=1,
                ),
            )
        ],
    )

    source_document = gen_gmn_startregistartion(payload)

    assert source_document.tag == "sourceDocument"
    assert source_document.find(".//measuringPoint") is not None


def test_gld_startregistration_accepts_nested_dataclasses():
    payload = GldStartRegistrationData(
        objectIdAccountableParty="obj-003",
        monitoringPoints=[
            GldMonitoringPointRef(
                broId="GMW000000009",
                tubeNumber=1,
            )
        ],
    )

    source_document = gen_gld_startregistration(
        payload,
        ns_regreq_map_gld2,
        codespace_map_gld1,
    )

    xml_text = etree.tostring(source_document, encoding="unicode")
    assert "GLD_StartRegistration" in xml_text
    assert "monitoringPoint" in xml_text
