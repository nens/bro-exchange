from lxml import etree

from bro_exchange.broxml.mappings import codespace_map_gar1, ns_regreq_map_gar2
from bro_exchange.broxml.request_helpers import coerce_srcdocdata
from bro_exchange.checks import check_missing_args

from .constructables import (
    gen_field_research,
    gen_groundwatermonitoringnet,
    gen_laboratory_analysis,
    gen_monitoringpoint,
)


def gen_gar(data):
    """Build the ``GAR`` sourceDocument, shared by registration and replace requests."""

    data = coerce_srcdocdata(data)

    arglist = {
        "objectIdAccountableParty": "obligated",
        "qualityControlMethod": "obligated",
        "gmwBroId": "obligated",
        "tubeNumber": "obligated",
        "fieldResearch": "obligated",
    }

    check_missing_args(data, arglist, "gen_gar")

    sourceDocument = etree.Element("sourceDocument")
    GAR = etree.SubElement(
        sourceDocument,
        "GAR",
        attrib={("{%s}" % ns_regreq_map_gar2["gml"]) + "id": "id_0001"},
    )

    objectIdAccountableParty = etree.SubElement(GAR, "objectIdAccountableParty")
    objectIdAccountableParty.text = str(data["objectIdAccountableParty"])

    qualityControlMethod = etree.SubElement(
        GAR,
        "qualityControlMethod",
        codeSpace=codespace_map_gar1["qualityControlMethod"],
    )
    qualityControlMethod.text = str(data["qualityControlMethod"])

    for net_bro_id in data.get("groundwaterMonitoringNets", []):
        GAR.append(gen_groundwatermonitoringnet(net_bro_id))

    GAR.append(gen_monitoringpoint(data["gmwBroId"], data["tubeNumber"]))

    GAR.append(gen_field_research(coerce_srcdocdata(data["fieldResearch"])))

    for lab_analysis in data.get("laboratoryAnalyses", []):
        GAR.append(gen_laboratory_analysis(coerce_srcdocdata(lab_analysis)))

    return sourceDocument
