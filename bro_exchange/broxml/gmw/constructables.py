import uuid

from lxml import etree

from bro_exchange import check_missing_args

# =============================================================================
# General info
# =============================================================================

# https://schema.broservices.nl/xsd/isgmw/1.1/isgmw-messages.xsd

# %%


def gen_wellconstructiondate(data, nsmap):
    WellConstructionDate = etree.Element(
        ("{%s}" % nsmap["ns"]) + "wellConstructionDate", nsmap=nsmap
    )
    date = etree.SubElement(
        WellConstructionDate, ("{%s}" % nsmap["ns1"]) + "date", nsmap=nsmap
    )
    date.text = data["wellConstructionDate"]
    return WellConstructionDate


def gen_eventdate(data, nsmap):
    eventDate = etree.Element(("{%s}" % nsmap["ns"]) + "eventDate", nsmap=nsmap)
    date = etree.SubElement(eventDate, ("{%s}" % nsmap["ns1"]) + "date", nsmap=nsmap)
    date.text = data["eventDate"]
    return eventDate


def gen_removaldate(data, nsmap):
    wellRemovalDate = etree.Element(
        ("{%s}" % nsmap["ns"]) + "wellRemovalDate", nsmap=nsmap
    )
    date = etree.SubElement(
        wellRemovalDate, ("{%s}" % nsmap["ns1"]) + "date", nsmap=nsmap
    )
    date.text = data["wellRemovalDate"]
    return wellRemovalDate


# %%


def gen_deliveredlocation(data, nsmap, codespacemap):
    """

    Parameters
    ----------
    data : dictionary, with deliveredLocation item.
        The deliveredLocation item itself is also a
        dictionary containing the following items:
            X: xcoordinate
            Y: ycoordinate
            horizontalPositioningMethod: horizontalPositioningMethod
    nsmap : dictionary
        namespace mapping
    codespacemap: dictionary
        codespace mapping

    Returns
    -------
    subelement structure to pass in the deliveredLocation element

    Note:
    -------
    The coordinate system is restricted to EPSG::28992
    """

    arglist = {
        "X": "obligated",
        "Y": "obligated",
        "horizontalPositioningMethod": "obligated",
    }

    check_missing_args(data["deliveredLocation"], arglist, "gen_deliveredlocation")

    deliveredLocation = etree.Element(
        ("{%s}" % nsmap["ns"]) + "deliveredLocation", nsmap=nsmap
    )

    location = etree.SubElement(
        deliveredLocation,
        ("{%s}" % nsmap["ns2"]) + "location",
        nsmap=nsmap,
        attrib={
            ("{%s}" % nsmap["ns3"]) + "id": "id-" + str(uuid.uuid4()),
            "srsName": "urn:ogc:def:crs:EPSG::28992",
        },
    )

    pos = etree.SubElement(location, ("{%s}" % nsmap["ns3"]) + "pos", nsmap=nsmap)

    pos.text = "{X} {Y}".format(
        X=str(data["deliveredLocation"]["X"]), Y=str(data["deliveredLocation"]["Y"])
    )

    horizontalPositioningMethod = etree.SubElement(
        deliveredLocation,
        ("{%s}" % nsmap["ns2"]) + "horizontalPositioningMethod",
        nsmap=nsmap,
        codeSpace=codespacemap["horizontalPositioningMethod"],
    )
    horizontalPositioningMethod.text = data["deliveredLocation"][
        "horizontalPositioningMethod"
    ]

    return deliveredLocation


# %%


def gen_deliveredverticalposition(data, nsmap, codespacemap):
    arglist = {
        "localVerticalReferencePoint": "obligated",
        "offset": "obligated",
        "verticalDatum": "obligated",
        "groundLevelPosition": "obligated",
        "groundLevelPositioningMethod": "obligated",
    }

    check_missing_args(
        data["deliveredVerticalPosition"], arglist, "gen_deliveredverticalposition"
    )

    deliveredVerticalPosition = etree.Element(
        ("{%s}" % nsmap["ns"]) + "deliveredVerticalPosition", nsmap=nsmap
    )
    localVerticalReferencePoint = etree.SubElement(
        deliveredVerticalPosition,
        ("{%s}" % nsmap["ns2"]) + "localVerticalReferencePoint",
        nsmap=nsmap,
        codeSpace=codespacemap["localVerticalReferencePoint"],
    )
    localVerticalReferencePoint.text = data["deliveredVerticalPosition"][
        "localVerticalReferencePoint"
    ]

    offset = etree.SubElement(
        deliveredVerticalPosition,
        ("{%s}" % nsmap["ns2"]) + "offset",
        nsmap=nsmap,
        uom="m",
    )
    offset.text = str(data["deliveredVerticalPosition"]["offset"])

    verticalDatum = etree.SubElement(
        deliveredVerticalPosition,
        ("{%s}" % nsmap["ns2"]) + "verticalDatum",
        nsmap=nsmap,
        codeSpace="urn:bro:gmw:VerticalDatum",
    )
    verticalDatum.text = data["deliveredVerticalPosition"]["verticalDatum"]

    groundLevelPosition = etree.SubElement(
        deliveredVerticalPosition,
        ("{%s}" % nsmap["ns2"]) + "groundLevelPosition",
        nsmap=nsmap,
        uom="m",
    )
    groundLevelPosition.text = str(
        data["deliveredVerticalPosition"]["groundLevelPosition"]
    )

    groundLevelPositioningMethod = etree.SubElement(
        deliveredVerticalPosition,
        ("{%s}" % nsmap["ns2"]) + "groundLevelPositioningMethod",
        nsmap=nsmap,
        codeSpace=codespacemap["groundLevelPositioningMethod"],
    )
    groundLevelPositioningMethod.text = data["deliveredVerticalPosition"][
        "groundLevelPositioningMethod"
    ]

    return deliveredVerticalPosition


# %%


def gen_materialused(data, tube, nsmap, codespacemap, sourcedoctype):
    if sourcedoctype in ["GMW_Construction", "construction"]:
        arglist = {
            "tubePackingMaterial": "obligated",
            "tubeMaterial": "obligated",
            "glue": "obligated",
        }

    elif sourcedoctype in ["GMW_Lengthening", "lengthening"]:
        arglist = {
            "tubePackingMaterial": "optional",
            "tubeMaterial": "optional",
            "glue": "optional",
        }

    check_missing_args(
        data["monitoringTubes"][tube]["materialUsed"],
        arglist,
        f"gen_monitoringtube, tube with index {str(tube)}, gen_materialused",
    )

    materialUsed = etree.Element(("{%s}" % nsmap["ns"]) + "materialUsed", nsmap=nsmap)

    if "tubePackingMaterial" in list(
        data["monitoringTubes"][tube]["materialUsed"].keys()
    ):
        tubePackingMaterial = etree.SubElement(
            materialUsed,
            ("{%s}" % nsmap["ns2"]) + "tubePackingMaterial",
            nsmap=nsmap,
            codeSpace=codespacemap["tubePackingMaterial"],
        )
        tubePackingMaterial.text = str(
            data["monitoringTubes"][tube]["materialUsed"]["tubePackingMaterial"]
        )

    if "tubeMaterial" in list(data["monitoringTubes"][tube]["materialUsed"].keys()):
        tubeMaterial = etree.SubElement(
            materialUsed,
            ("{%s}" % nsmap["ns2"]) + "tubeMaterial",
            nsmap=nsmap,
            codeSpace=codespacemap["tubeMaterial"],
        )
        tubeMaterial.text = str(
            data["monitoringTubes"][tube]["materialUsed"]["tubeMaterial"]
        )

    if "glue" in list(data["monitoringTubes"][tube]["materialUsed"].keys()):
        glue = etree.SubElement(
            materialUsed,
            ("{%s}" % nsmap["ns2"]) + "glue",
            nsmap=nsmap,
            codeSpace="urn:bro:gmw:Glue",
        )
        glue.text = str(data["monitoringTubes"][tube]["materialUsed"]["glue"])

    return materialUsed


# %%


def gen_screen(data, tube, nsmap, codespacemap):
    arglist = {"screenLength": "obligated", "sockMaterial": "obligated"}

    check_missing_args(
        data["monitoringTubes"][tube]["screen"],
        arglist,
        f"gen_monitoringtube, tube with index {str(tube)}, gen_screen",
    )

    screen = etree.Element(("{%s}" % nsmap["ns"]) + "screen", nsmap=nsmap)

    screenLength = etree.SubElement(
        screen, ("{%s}" % nsmap["ns"]) + "screenLength", nsmap=nsmap, uom="m"
    )
    screenLength.text = str(data["monitoringTubes"][tube]["screen"]["screenLength"])

    sockmaterial = etree.SubElement(
        screen,
        ("{%s}" % nsmap["ns"]) + "sockMaterial",
        nsmap=nsmap,
        codeSpace=codespacemap["sockMaterial"],
    )
    sockmaterial.text = str(data["monitoringTubes"][tube]["screen"]["sockMaterial"])

    return screen


# %%


def gen_plaintubepart(data, tube, nsmap, sourcedoctype):
    arglist = {"plainTubePartLength": "obligated"}

    check_missing_args(
        data["monitoringTubes"][tube]["plainTubePart"],
        arglist,
        f"gen_monitoringtube, tube with index {str(tube)}, gen_plaintubepart",
    )

    plainTubePart = etree.Element(("{%s}" % nsmap["ns"]) + "plainTubePart", nsmap=nsmap)

    plainTubePartLength = etree.SubElement(
        plainTubePart,
        ("{%s}" % nsmap["ns2"]) + "plainTubePartLength",
        nsmap=nsmap,
        uom="m",
    )
    plainTubePartLength.text = str(
        data["monitoringTubes"][tube]["plainTubePart"]["plainTubePartLength"]
    )

    return plainTubePart


# %%


def gen_sedimentsump(data, tube, nsmap):
    arglist = {"sedimentSumpLength": "obligated"}

    check_missing_args(
        data["monitoringTubes"][tube]["sedimentSump"],
        arglist,
        f"gen_monitoringtube, tube with index {str(tube)}, gen_sedimentsump",
    )

    sedimentSump = etree.Element(("{%s}" % nsmap["ns"]) + "sedimentSump", nsmap=nsmap)

    sedimentSumpLength = etree.SubElement(
        sedimentSump,
        ("{%s}" % nsmap["ns2"]) + "sedimentSumpLength",
        nsmap=nsmap,
        uom="m",
    )
    sedimentSumpLength.text = str(
        data["monitoringTubes"][tube]["sedimentSump"]["sedimentSumpLength"]
    )

    return sedimentSump


# %%
def gen_electrode(data, tube, geoOhmCableId, electrode, nsmap, codespacemap):
    arglist = {
        "electrodeNumber": "obligated",
        "electrodePackingMaterial": "obligated",
        "electrodeStatus": "obligated",
        "electrodePosition": "obligated",
    }

    targetdata = data["monitoringTubes"][tube]["geoOhmCables"][geoOhmCableId][
        "electrodes"
    ][electrode]

    check_missing_args(
        targetdata,
        arglist,
        f"gen_monitoringtube, tube with index {str(tube)}, geoOhmCable with index {str(geoOhmCableId)}, electrode with index {str(electrode)}",
    )

    electrode = etree.Element(("{%s}" % nsmap["ns"]) + "electrode", nsmap=nsmap)

    electrodeNumber = etree.SubElement(
        electrode, ("{%s}" % nsmap["ns2"]) + "electrodeNumber", nsmap=nsmap
    )
    electrodeNumber.text = str(targetdata["electrodeNumber"])

    electrodePackingMaterial = etree.SubElement(
        electrode,
        ("{%s}" % nsmap["ns2"]) + "electrodePackingMaterial",
        nsmap=nsmap,
        codeSpace=codespacemap["electrodePackingMaterial"],
    )
    electrodePackingMaterial.text = str(targetdata["electrodePackingMaterial"])

    electrodeStatus = etree.SubElement(
        electrode,
        ("{%s}" % nsmap["ns2"]) + "electrodeStatus",
        nsmap=nsmap,
        codeSpace=codespacemap["electrodeStatus"],
    )
    electrodeStatus.text = str(targetdata["electrodeStatus"])

    electrodePosition = etree.SubElement(
        electrode, ("{%s}" % nsmap["ns2"]) + "electrodePosition", nsmap=nsmap, uom="m"
    )
    electrodePosition.text = str(targetdata["electrodePosition"])

    return electrode


def adjust_electrode(data, electrode, nsmap, codespacemap):
    arglist = {
        "tubeNumber": "obligated",
        "cableNumber": "obligated",
        "electrodeNumber": "obligated",
        "electrodeStatus": "obligated",
    }

    targetdata = data["electrodes"][electrode]

    check_missing_args(
        targetdata,
        arglist,
        "gen_monitoringtube, tube with index {}, geoOhmCable with index {}, electrode with index {}".format(
            str(targetdata["tubeNumber"]),
            str(targetdata["cableNumber"]),
            str(targetdata["electrodeNumber"]),
        ),
    )

    electrode = etree.Element(("{%s}" % nsmap["ns"]) + "electrode", nsmap=nsmap)

    tubeNumber = etree.SubElement(
        electrode, ("{%s}" % nsmap["ns"]) + "tubeNumber", nsmap=nsmap
    )
    tubeNumber.text = str(targetdata["tubeNumber"])

    cableNumber = etree.SubElement(
        electrode, ("{%s}" % nsmap["ns"]) + "cableNumber", nsmap=nsmap
    )
    cableNumber.text = str(targetdata["cableNumber"])

    electrodeNumber = etree.SubElement(
        electrode, ("{%s}" % nsmap["ns"]) + "electrodeNumber", nsmap=nsmap
    )
    electrodeNumber.text = str(targetdata["electrodeNumber"])

    electrodeStatus = etree.SubElement(
        electrode,
        ("{%s}" % nsmap["ns"]) + "electrodeStatus",
        nsmap=nsmap,
        codeSpace=codespacemap["electrodeStatus"],
    )
    electrodeStatus.text = str(targetdata["electrodeStatus"])

    return electrode


# %%


def gen_geoohmcable(data, tube, geoOhmCableId, nsmap, codespacemap):
    arglist = {"cableNumber": "obligated", "electrodes": "obligated"}

    check_missing_args(
        data["monitoringTubes"][tube]["geoOhmCables"][geoOhmCableId],
        arglist,
        f"gen_monitoringtube, tube with index {str(tube)}, gen_geoohmcable, geoOhmCableId {str(geoOhmCableId)}",
    )

    if (
        len(data["monitoringTubes"][tube]["geoOhmCables"][geoOhmCableId]["electrodes"])
        < 2
    ):
        raise Exception(
            "Not enough electrodes provided for geoOhmCable, at least 2 electrodes should be provided"
        )

    else:
        geoOhmCable = etree.Element(("{%s}" % nsmap["ns"]) + "geoOhmCable", nsmap=nsmap)

        cableNumber = etree.SubElement(
            geoOhmCable, ("{%s}" % nsmap["ns"]) + "cableNumber", nsmap=nsmap
        )
        cableNumber.text = str(geoOhmCableId + 1)

        electrodes = {}
        for electrode in range(
            len(
                data["monitoringTubes"][tube]["geoOhmCables"][geoOhmCableId][
                    "electrodes"
                ]
            )
        ):
            electrodes[f"electrode{str(electrode)}"] = gen_electrode(
                data, tube, geoOhmCableId, electrode, nsmap, codespacemap
            )
            geoOhmCable.append(electrodes[f"electrode{str(electrode)}"])

        return geoOhmCable


# %%


def gen_monitoringtube(data, tube, nsmap, codespacemap, sourcedoctype):
    """

    Parameters
    ----------
    data : dictionary, with monitoringtubes item.
        The monitoringtubes item consits of a list with dictionaries,
        in which each dictionary contains the attribute data of a single
        monitoringtube. The required and optional items are listed within
        the arglist in this function.
    tube : int
        monituringtube index in list of available monitoringtubes. A
        monitoringTube element will be created for the selected
        monitoringtube.
    nsmap : dictionary
        namespace mapping
    codespacemap: dictionary
        codespace mapping

    Returns
    -------
    subelement structure to pass in the monitoringtube element for the
    selected monitoringtube

    """

    if sourcedoctype in ["GMW_Construction", "construction"]:
        arglist = {
            "tubeNumber": "obligated",
            "tubeType": "obligated",
            "artesianWellCapPresent": "obligated",
            "sedimentSumpPresent": "obligated",
            "numberOfGeoOhmCables": "obligated",
            "tubeTopDiameter": "obligated",
            "variableDiameter": "obligated",
            "tubeStatus": "obligated",
            "tubeTopPosition": "obligated",
            "tubeTopPositioningMethod": "obligated",
            "materialUsed": "obligated",
            "screen": "obligated",
            "plainTubePart": "obligated",
            "sedimentSump": "optional",
            "geoOhmCables": "optional",
        }
    elif sourcedoctype in [
        "GMW_Positions",
        "GMW_PositionsMeasuring",
        "positions",
        "positionsMeasuring",
    ]:
        arglist = {
            "tubeNumber": "obligated",
            "tubeTopPosition": "obligated",
            "tubeTopPositioningMethod": "obligated",
        }
    elif sourcedoctype in [
        "GMW_Lengthening",
        "GMW_Shortening",
        "lengthening",
        "shortening",
    ]:
        arglist = {
            "tubeNumber": "obligated",
            "tubeTopPosition": "obligated",
            "tubeTopPositioningMethod": "obligated",
            "plainTubePart": "obligated",
        }
    elif sourcedoctype in ["GMW_TubeStatus", "tubeStatus"]:
        arglist = {"tubeNumber": "obligated", "tubeStatus": "obligated"}

    check_missing_args(
        data["monitoringTubes"][tube],
        arglist,
        f"gen_monitoringtube, tube with index {str(tube)}",
    )

    monitoringTube = etree.Element(
        ("{%s}" % nsmap["ns"]) + "monitoringTube", nsmap=nsmap
    )

    if sourcedoctype in ["GMW_Construction", "construction"]:
        if "tubeNumber" in list(data["monitoringTubes"][tube].keys()):
            tubeNumber = etree.SubElement(
                monitoringTube, ("{%s}" % nsmap["ns"]) + "tubeNumber", nsmap=nsmap
            )
            tubeNumber.text = str(data["monitoringTubes"][tube]["tubeNumber"])

        if "tubeType" in list(data["monitoringTubes"][tube].keys()):
            tubeType = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "tubeType",
                nsmap=nsmap,
                codeSpace=codespacemap["tubeType"],
            )
            tubeType.text = data["monitoringTubes"][tube]["tubeType"]

        if "artesianWellCapPresent" in list(data["monitoringTubes"][tube].keys()):
            artesianWellCapPresent = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "artesianWellCapPresent",
                nsmap=nsmap,
            )
            artesianWellCapPresent.text = data["monitoringTubes"][tube][
                "artesianWellCapPresent"
            ]

        if "sedimentSumpPresent" in list(data["monitoringTubes"][tube].keys()):
            sedimentSumpPresent = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "sedimentSumpPresent",
                nsmap=nsmap,
            )
            sedimentSumpPresent.text = data["monitoringTubes"][tube][
                "sedimentSumpPresent"
            ]

        if "numberOfGeoOhmCables" in list(data["monitoringTubes"][tube].keys()):
            numberOfGeoOhmCables = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "numberOfGeoOhmCables",
                nsmap=nsmap,
            )
            numberOfGeoOhmCables.text = str(
                data["monitoringTubes"][tube]["numberOfGeoOhmCables"]
            )

        if "tubeTopDiameter" in list(data["monitoringTubes"][tube].keys()):
            if data["monitoringTubes"][tube]["tubeTopDiameter"] is not None:
                tubeTopDiameter = etree.SubElement(
                    monitoringTube,
                    ("{%s}" % nsmap["ns"]) + "tubeTopDiameter",
                    nsmap=nsmap,
                    uom="mm",
                )
                tubeTopDiameter.text = str(
                    data["monitoringTubes"][tube]["tubeTopDiameter"]
                )
            else:
                tubeTopDiameter = etree.SubElement(
                    monitoringTube,
                    ("{%s}" % nsmap["ns"]) + "tubeTopDiameter",
                    nsmap=nsmap,
                    uom="mm",
                    attrib={("{%s}" % nsmap["xsi"]) + "nil": "true"},
                )

        if "variableDiameter" in list(data["monitoringTubes"][tube].keys()):
            variableDiameter = etree.SubElement(
                monitoringTube, ("{%s}" % nsmap["ns"]) + "variableDiameter", nsmap=nsmap
            )
            variableDiameter.text = str(
                data["monitoringTubes"][tube]["variableDiameter"]
            )

        if "tubeStatus" in list(data["monitoringTubes"][tube].keys()):
            tubeStatus = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "tubeStatus",
                nsmap=nsmap,
                codeSpace=codespacemap["tubeStatus"],
            )
            tubeStatus.text = data["monitoringTubes"][tube]["tubeStatus"]

        if "tubeTopPosition" in list(data["monitoringTubes"][tube].keys()):
            tubeTopPosition = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "tubeTopPosition",
                nsmap=nsmap,
                uom="m",
            )
            tubeTopPosition.text = str(data["monitoringTubes"][tube]["tubeTopPosition"])

        if "tubeTopPositioningMethod" in list(data["monitoringTubes"][tube].keys()):
            tubeTopPositioningMethod = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "tubeTopPositioningMethod",
                nsmap=nsmap,
                codeSpace=codespacemap["tubeTopPositioningMethod"],
            )
            tubeTopPositioningMethod.text = str(
                data["monitoringTubes"][tube]["tubeTopPositioningMethod"]
            )

            # obligated constructables:
        if "materialUsed" in list(data["monitoringTubes"][tube].keys()):
            materialUsed = gen_materialused(
                data, tube, nsmap, codespacemap, sourcedoctype
            )
            monitoringTube.append(materialUsed)

        if "screen" in list(data["monitoringTubes"][tube].keys()):
            screen = gen_screen(data, tube, nsmap, codespacemap)
            monitoringTube.append(screen)

        if "plainTubePart" in list(data["monitoringTubes"][tube].keys()):
            plainTubePart = gen_plaintubepart(data, tube, nsmap, sourcedoctype)
            monitoringTube.append(plainTubePart)

        # optional constructables:
        if "sedimentSump" in list(data["monitoringTubes"][tube].keys()):
            sedimentSump = gen_sedimentsump(data, tube, nsmap)
            monitoringTube.append(sedimentSump)

        if "geoOhmCables" in list(data["monitoringTubes"][tube].keys()):
            geoOhmCables = {}

            for geoOhmCableId in range(
                len(data["monitoringTubes"][tube]["geoOhmCables"])
            ):
                geoOhmCables[f"geoOhmCable{str(geoOhmCableId)}"] = gen_geoohmcable(
                    data, tube, geoOhmCableId, nsmap, codespacemap
                )
                monitoringTube.append(geoOhmCables[f"geoOhmCable{str(geoOhmCableId)}"])

    elif sourcedoctype in [
        "GMW_Lengthening",
        "GMW_Shortening",
        "lengthening",
        "shortening",
    ]:
        if "tubeNumber" in list(data["monitoringTubes"][tube].keys()):
            tubeNumber = etree.SubElement(
                monitoringTube, ("{%s}" % nsmap["ns"]) + "tubeNumber", nsmap=nsmap
            )
            tubeNumber.text = str(data["monitoringTubes"][tube]["tubeNumber"])

        if sourcedoctype not in ["GMW_Shortening", "shortening"]:
            if "variableDiameter" in list(data["monitoringTubes"][tube].keys()):
                variableDiameter = etree.SubElement(
                    monitoringTube,
                    ("{%s}" % nsmap["ns"]) + "variableDiameter",
                    nsmap=nsmap,
                )
                variableDiameter.text = str(
                    data["monitoringTubes"][tube]["variableDiameter"]
                )

            if "tubeStatus" in list(data["monitoringTubes"][tube].keys()):
                tubeStatus = etree.SubElement(
                    monitoringTube,
                    ("{%s}" % nsmap["ns"]) + "tubeStatus",
                    nsmap=nsmap,
                    codeSpace=codespacemap["tubeStatus"],
                )
                tubeStatus.text = data["monitoringTubes"][tube]["tubeStatus"]

        if "tubeTopPosition" in list(data["monitoringTubes"][tube].keys()):
            tubeTopPosition = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "tubeTopPosition",
                nsmap=nsmap,
                uom="m",
            )
            tubeTopPosition.text = str(data["monitoringTubes"][tube]["tubeTopPosition"])

        if "tubeTopPositioningMethod" in list(data["monitoringTubes"][tube].keys()):
            tubeTopPositioningMethod = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "tubeTopPositioningMethod",
                nsmap=nsmap,
                codeSpace=codespacemap["tubeTopPositioningMethod"],
            )
            tubeTopPositioningMethod.text = str(
                data["monitoringTubes"][tube]["tubeTopPositioningMethod"]
            )

        if sourcedoctype not in ["GMW_Shortening", "shortening"]:
            if "tubeMaterial" in list(
                data["monitoringTubes"][tube]["materialUsed"].keys()
            ):
                tubeMaterial = etree.SubElement(
                    monitoringTube,
                    ("{%s}" % nsmap["ns"]) + "tubeMaterial",
                    nsmap=nsmap,
                    codeSpace=codespacemap["tubeMaterial"],
                )
                tubeMaterial.text = str(
                    data["monitoringTubes"][tube]["materialUsed"]["tubeMaterial"]
                )

            if "glue" in list(data["monitoringTubes"][tube]["materialUsed"].keys()):
                glue = etree.SubElement(
                    monitoringTube,
                    ("{%s}" % nsmap["ns"]) + "glue",
                    nsmap=nsmap,
                    codeSpace="urn:bro:gmw:Glue",
                )
                glue.text = str(data["monitoringTubes"][tube]["materialUsed"]["glue"])

        if "plainTubePartLength" in list(
            data["monitoringTubes"][tube]["plainTubePart"].keys()
        ):
            plainTubePartLength = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "plainTubePartLength",
                nsmap=nsmap,
                uom="m",
            )
            plainTubePartLength.text = str(
                data["monitoringTubes"][tube]["plainTubePart"]["plainTubePartLength"]
            )

    elif sourcedoctype in [
        "GMW_Positions",
        "GMW_PositionsMeasuring",
        "positions",
        "positionsMeasuring",
    ]:
        if "tubeNumber" in list(data["monitoringTubes"][tube].keys()):
            tubeNumber = etree.SubElement(
                monitoringTube, ("{%s}" % nsmap["ns"]) + "tubeNumber", nsmap=nsmap
            )
            tubeNumber.text = str(data["monitoringTubes"][tube]["tubeNumber"])

        if "tubeTopPosition" in list(data["monitoringTubes"][tube].keys()):
            tubeTopPosition = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "tubeTopPosition",
                nsmap=nsmap,
                uom="m",
            )
            tubeTopPosition.text = str(data["monitoringTubes"][tube]["tubeTopPosition"])

        if "tubeTopPositioningMethod" in list(data["monitoringTubes"][tube].keys()):
            tubeTopPositioningMethod = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "tubeTopPositioningMethod",
                nsmap=nsmap,
                codeSpace=codespacemap["tubeTopPositioningMethod"],
            )
            tubeTopPositioningMethod.text = str(
                data["monitoringTubes"][tube]["tubeTopPositioningMethod"]
            )

    elif sourcedoctype in ["GMW_TubeStatus", "tubeStatus"]:
        if "tubeNumber" in list(data["monitoringTubes"][tube].keys()):
            tubeNumber = etree.SubElement(
                monitoringTube, ("{%s}" % nsmap["ns"]) + "tubeNumber", nsmap=nsmap
            )
            tubeNumber.text = str(data["monitoringTubes"][tube]["tubeNumber"])

        if "tubeStatus" in list(data["monitoringTubes"][tube].keys()):
            tubeStatus = etree.SubElement(
                monitoringTube,
                ("{%s}" % nsmap["ns"]) + "tubeStatus",
                nsmap=nsmap,
                codeSpace=codespacemap["tubeStatus"],
            )
            tubeStatus.text = data["monitoringTubes"][tube]["tubeStatus"]

    return monitoringTube
