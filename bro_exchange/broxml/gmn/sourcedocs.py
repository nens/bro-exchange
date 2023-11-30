from lxml import etree

from bro_exchange import check_missing_args
from bro_exchange.broxml.mappings import (  # mappings
    codespace_map_gmn1,
    ns_regreq_map_gmn2,
)

from .constructables import (
    gen_enddate,
    gen_eventdate,
    gen_measuringpoint,
    gen_startdatemonitoring,
)


def gen_gmn_startregistartion(data):
    arglist = {
        "objectIdAccountableParty": "obligated",
        "name": "obligated",
        "deliveryContext": "obligated",
        "monitoringPurpose": "obligated",
        "groundwaterAspect": "obligated",
        "startDateMonitoring": "obligated",
        "measuringPoints": "obligated",
    }

    # Note: mapSheetCode is a valid optional argument that hasn't been included yet

    constructables = ["startDateMonitoring", "measuringPoints"]

    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, "gen_gmn_construction")

    sourceDocument = etree.Element("sourceDocument")
    GMN_StartRegistration = etree.SubElement(
        sourceDocument,
        "GMN_StartRegistration",
        attrib={("{%s}" % ns_regreq_map_gmn2["gml"]) + "id": "id_0001"},
    )

    # GMW_Construction subelements:
    GMN_StartRegistration_subelements = {}
    for arg in data.keys():
        if arg not in constructables:
            if arg in codespace_map_gmn1.keys():
                GMN_StartRegistration_subelements[arg] = etree.SubElement(
                    GMN_StartRegistration, arg, codeSpace=codespace_map_gmn1[arg]
                )
                GMN_StartRegistration_subelements[arg].text = str(data[arg])
            else:
                GMN_StartRegistration_subelements[arg] = etree.SubElement(
                    GMN_StartRegistration, arg
                )
                GMN_StartRegistration_subelements[arg].text = str(data[arg])

        else:
            if arg == "startDateMonitoring":
                GMN_StartRegistration_subelements[arg] = gen_startdatemonitoring(
                    data, ns_regreq_map_gmn2
                )
                GMN_StartRegistration.append(GMN_StartRegistration_subelements[arg])

            elif arg == "measuringPoints":
                if len(data["measuringPoints"]) < 1:
                    raise Exception(
                        "No measuringPoints provided in input, at least 1 measuringPoint should be provided"
                    )
                else:
                    for mp in range(len(data[arg])):
                        GMN_StartRegistration_subelements[
                            f"measuringPoint{str(mp)}"
                        ] = gen_measuringpoint(data, ns_regreq_map_gmn2, mp)
                        GMN_StartRegistration.append(
                            GMN_StartRegistration_subelements[
                                f"measuringPoint{str(mp)}"
                            ]
                        )

    return sourceDocument


def gen_gmn_measuringpoint(data):
    arglist = {
        "eventDate": "obligated",
        "measuringPoint": "obligated",
    }

    # Note: mapSheetCode is a valid optional argument that hasn't been included yet

    constructables = ["eventDate", "measuringPoint"]

    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, "gen_gmn_construction")

    sourceDocument = etree.Element("sourceDocument")
    GMN_MeasuringPoint = etree.SubElement(
        sourceDocument,
        "GMN_MeasuringPoint",
        attrib={("{%s}" % ns_regreq_map_gmn2["gml"]) + "id": "id_0001"},
    )

    # GMW_Construction subelements:
    GMN_MeasuringPoint_subelements = {}
    for arg in data.keys():
        if arg not in constructables:
            if arg in codespace_map_gmn1.keys():
                GMN_MeasuringPoint_subelements[arg] = etree.SubElement(
                    GMN_MeasuringPoint, arg, codeSpace=codespace_map_gmn1[arg]
                )
                GMN_MeasuringPoint_subelements[arg].text = str(data[arg])
            else:
                GMN_MeasuringPoint_subelements[arg] = etree.SubElement(
                    GMN_MeasuringPoint, arg
                )
                GMN_MeasuringPoint_subelements[arg].text = str(data[arg])

        else:
            if arg == "eventDate":
                GMN_MeasuringPoint_subelements[arg] = gen_eventdate(
                    data, ns_regreq_map_gmn2
                )
                GMN_MeasuringPoint.append(GMN_MeasuringPoint_subelements[arg])

            elif arg == "measuringPoint":
                GMN_MeasuringPoint_subelements[
                    f"measuringPoint{str(0)}"
                ] = gen_measuringpoint(data, ns_regreq_map_gmn2)
                GMN_MeasuringPoint.append(
                    GMN_MeasuringPoint_subelements[f"measuringPoint{str(0)}"]
                )

    return sourceDocument


def gen_gmn_measuringpoint_enddate(data):
    arglist = {
        "eventDate": "obligated",
        "measuringPoint": "obligated",
    }

    # Note: mapSheetCode is a valid optional argument that hasn't been included yet

    constructables = ["eventDate", "measuringPoint"]

    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, "gen_gmn_construction")

    sourceDocument = etree.Element("sourceDocument")
    GMN_MeasuringPointEndDate = etree.SubElement(
        sourceDocument,
        "GMN_MeasuringPointEndDate",
        attrib={("{%s}" % ns_regreq_map_gmn2["gml"]) + "id": "id_0001"},
    )

    # GMW_Construction subelements:
    GMN_MeasuringPointEndDate_subelements = {}
    for arg in data.keys():
        if arg == "eventDate":
            GMN_MeasuringPointEndDate_subelements[arg] = gen_eventdate(
                data, ns_regreq_map_gmn2
            )
            GMN_MeasuringPointEndDate.append(GMN_MeasuringPointEndDate_subelements[arg])
        elif arg == "measuringPoint":
            GMN_MeasuringPointEndDate_subelements[arg] = etree.Element(
                "measuringPointCode"
            )
            GMN_MeasuringPointEndDate_subelements[arg].text = data[arg]
            GMN_MeasuringPointEndDate.append(GMN_MeasuringPointEndDate_subelements[arg])

    return sourceDocument


def gen_gmn_closure(data):
    arglist = {
        "endDateMonitoring": "obligated",
    }

    # Note: mapSheetCode is a valid optional argument that hasn't been included yet

    constructables = ["endDateMonitoring"]

    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, "gen_gmn_construction")
    sourceDocument = etree.Element("sourceDocument")
    GMN_MeasuringPointEndDate = etree.SubElement(
        sourceDocument,
        "GMN_Closure",
        attrib={("{%s}" % ns_regreq_map_gmn2["gml"]) + "id": "id_0001"},
    )

    # GMW_Construction subelements:
    GMN_MeasuringPointEndDate_subelements = {}
    for arg in data.keys():
        if arg == "endDateMonitoring":
            GMN_MeasuringPointEndDate_subelements[arg] = gen_enddate(
                data, ns_regreq_map_gmn2
            )
            GMN_MeasuringPointEndDate.append(GMN_MeasuringPointEndDate_subelements[arg])

    return sourceDocument
