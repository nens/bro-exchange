# from gwmpy.broxml.mappings import ns_regreq_map # mappings

from lxml import etree

from bro_exchange.checks import check_missing_args

# %%


def gen_startdatemonitoring(data, nsmap):
    startDateMonitoring = etree.Element("startDateMonitoring")

    choice = data["startDateMonitoring"][1]
    text = data["startDateMonitoring"][0]

    if choice == "date":
        date = etree.SubElement(
            startDateMonitoring, ("{%s}" % nsmap["brocom"]) + "date", nsmap=nsmap
        )
        date.text = text
    elif choice == "year":
        date = etree.SubElement(
            startDateMonitoring, ("{%s}" % nsmap["brocom"]) + "year", nsmap=nsmap
        )
        date.text = text
    elif choice == "yearMonth":
        date = etree.SubElement(
            startDateMonitoring, ("{%s}" % nsmap["brocom"]) + "yearMonth", nsmap=nsmap
        )
        date.text = text
    elif text is None:
        date = etree.SubElement(
            startDateMonitoring, ("{%s}" % nsmap["brocom"]) + "voidReason", nsmap=nsmap
        )
        date.text = choice

    return startDateMonitoring


# %%


def gen_eventdate(data, nsmap):
    eventDate = etree.Element("eventDate")

    choice = data["eventDate"][1]
    text = data["eventDate"][0]

    if choice == "date":
        date = etree.SubElement(
            eventDate, ("{%s}" % nsmap["brocom"]) + "date", nsmap=nsmap
        )
        date.text = text
    elif choice == "year":
        date = etree.SubElement(
            eventDate, ("{%s}" % nsmap["brocom"]) + "year", nsmap=nsmap
        )
        date.text = text
    elif choice == "yearMonth":
        date = etree.SubElement(
            eventDate, ("{%s}" % nsmap["brocom"]) + "yearMonth", nsmap=nsmap
        )
        date.text = text
    elif text is None:
        date = etree.SubElement(
            eventDate, ("{%s}" % nsmap["brocom"]) + "voidReason", nsmap=nsmap
        )
        date.text = choice

    return eventDate


def gen_enddate(data, nsmap):
    endDate = etree.Element("endDateMonitoring")
    choice = data["endDateMonitoring"][1]
    text = data["endDateMonitoring"][0]

    if choice == "date":
        date = etree.SubElement(
            endDate, ("{%s}" % nsmap["brocom"]) + "date", nsmap=nsmap
        )
        date.text = text

    elif choice == "year":
        date = etree.SubElement(
            endDate, ("{%s}" % nsmap["brocom"]) + "year", nsmap=nsmap
        )
        date.text = text
    elif choice == "yearMonth":
        date = etree.SubElement(
            endDate, ("{%s}" % nsmap["brocom"]) + "yearMonth", nsmap=nsmap
        )
        date.text = text
    elif text is None:
        date = etree.SubElement(
            endDate, ("{%s}" % nsmap["brocom"]) + "voidReason", nsmap=nsmap
        )
        date.text = choice

    return endDate


# %%


def gen_measuringpoint(data, nsmap, mp=None):
    """

    Parameters
    ----------
    data : dictionary, with measuringpoints item.
        The measuringpoints item consits of a list with dictionaries,
        in which each dictionary contains the attribute data of a single
        monitoringtube. The required and optional items are listed within
        the arglist in this function.
    tube : int
        measuringpoint index in list of available measuringpoint. A
        measuringpoint element will be created for the selected
        measuringpoint.
    nsmap : dictionary
        namespace mapping
    codespacemap: dictionary
        codespace mapping

    Returns
    -------
    subelement structure to pass in the measuringpoint element for the
    selected measuringpoint

    """

    arglist = {"measuringPointCode": "obligated", "monitoringTube": "obligated"}

    if mp is not None:
        check_missing_args(
            data["measuringPoints"][mp],
            arglist,
            f"gen_monitoringtube, tube with index {str(mp)}",
        )

        measuringpoint = etree.Element("measuringPoint")

        measuringpoint_ = etree.SubElement(
            measuringpoint,
            "MeasuringPoint",
            attrib={("{%s}" % nsmap["gml"]) + "id": f"id_mp{str(mp)}"},
        )

        measuringpointcode = etree.SubElement(measuringpoint_, "measuringPointCode")
        measuringpointcode.text = data["measuringPoints"][mp]["measuringPointCode"]

        monitoringTube = etree.SubElement(measuringpoint_, "monitoringTube")

        GroundwaterMonitoringTube = etree.SubElement(
            monitoringTube,
            "GroundwaterMonitoringTube",
            attrib={("{%s}" % nsmap["gml"]) + "id": f"id_mpgwmt{str(mp)}"},
        )

        broId = etree.SubElement(GroundwaterMonitoringTube, "broId")
        broId.text = str(data["measuringPoints"][mp]["monitoringTube"]["broId"])

        tubeNumber = etree.SubElement(GroundwaterMonitoringTube, "tubeNumber")
        tubeNumber.text = str(
            data["measuringPoints"][mp]["monitoringTube"]["tubeNumber"]
        )

        return measuringpoint

    else:
        check_missing_args(
            data["measuringPoint"],
            arglist,
            f"gen_monitoringtube, tube with index {str(0)}",
        )

        measuringpoint = etree.Element("measuringPoint")

        measuringpoint_ = etree.SubElement(
            measuringpoint,
            "MeasuringPoint",
            attrib={("{%s}" % nsmap["gml"]) + "id": f"id_mp{str(0)}"},
        )

        measuringpointcode = etree.SubElement(measuringpoint_, "measuringPointCode")
        measuringpointcode.text = data["measuringPoint"]["measuringPointCode"]

        monitoringTube = etree.SubElement(measuringpoint_, "monitoringTube")

        GroundwaterMonitoringTube = etree.SubElement(
            monitoringTube,
            "GroundwaterMonitoringTube",
            attrib={("{%s}" % nsmap["gml"]) + "id": f"id_mpgwmt{str(0)}"},
        )

        broId = etree.SubElement(GroundwaterMonitoringTube, "broId")
        broId.text = str(data["measuringPoint"]["monitoringTube"]["broId"])

        tubeNumber = etree.SubElement(GroundwaterMonitoringTube, "tubeNumber")
        tubeNumber.text = str(data["measuringPoint"]["monitoringTube"]["tubeNumber"])

        return measuringpoint
