"""Element builders for nested GAR (Grondwateranalyserapport) source-document structures."""

from lxml import etree

GARCOM = "http://www.broservices.nl/xsd/garcommon/1.0"
BROCOM = "http://www.broservices.nl/xsd/brocommon/3.0"
XSI = "http://www.w3.org/2001/XMLSchema-instance"


def _garcom(tag: str) -> str:
    return f"{{{GARCOM}}}{tag}"


def _set_nil(element) -> None:
    element.set(f"{{{XSI}}}nil", "true")


def gen_groundwatermonitoringnet(bro_id: str) -> etree.Element:
    groundwaterMonitoringNet = etree.Element("groundwaterMonitoringNet")
    GroundwaterMonitoringNet = etree.SubElement(
        groundwaterMonitoringNet,
        _garcom("GroundwaterMonitoringNet"),
        attrib={"{http://www.opengis.net/gml/3.2}id": str(bro_id)},
    )
    broId = etree.SubElement(GroundwaterMonitoringNet, _garcom("broId"))
    broId.text = str(bro_id)
    return groundwaterMonitoringNet


def gen_monitoringpoint(gmw_bro_id: str, tube_number: str) -> etree.Element:
    monitoringPoint = etree.Element("monitoringPoint")
    GroundwaterMonitoringTube = etree.SubElement(
        monitoringPoint,
        _garcom("GroundwaterMonitoringTube"),
        attrib={
            "{http://www.opengis.net/gml/3.2}id": f"{gmw_bro_id}_{tube_number}"
        },
    )
    broId = etree.SubElement(GroundwaterMonitoringTube, _garcom("broId"))
    broId.text = str(gmw_bro_id)
    tubeNumber = etree.SubElement(GroundwaterMonitoringTube, _garcom("tubeNumber"))
    tubeNumber.text = str(tube_number)
    return monitoringPoint


def gen_field_measurement(measurement: dict) -> etree.Element:
    fieldMeasurement = etree.Element(_garcom("fieldMeasurement"))

    parameter = etree.SubElement(fieldMeasurement, _garcom("parameter"))
    parameter.text = str(measurement["parameter"])

    fieldMeasurementValue = etree.SubElement(
        fieldMeasurement,
        _garcom("fieldMeasurementValue"),
        attrib={"uom": str(measurement["unit"])},
    )
    fieldMeasurementValue.text = str(measurement["fieldMeasurementValue"])

    qualityControlStatus = etree.SubElement(
        fieldMeasurement,
        _garcom("qualityControlStatus"),
        attrib={"codeSpace": "urn:bro:gar:QualityControlStatus"},
    )
    qualityControlStatus.text = str(measurement["qualityControlStatus"])

    return fieldMeasurement


def gen_field_research(field_research: dict) -> etree.Element:
    fieldResearch = etree.Element("fieldResearch")

    samplingDateTime = etree.SubElement(fieldResearch, _garcom("samplingDateTime"))
    samplingDateTime.text = str(field_research["samplingDateTime"])

    samplingOperator = etree.SubElement(fieldResearch, _garcom("samplingOperator"))
    if field_research.get("samplingOperator"):
        chamberOfCommerceNumber = etree.SubElement(
            samplingOperator, f"{{{BROCOM}}}chamberOfCommerceNumber"
        )
        chamberOfCommerceNumber.text = str(field_research["samplingOperator"])
    else:
        _set_nil(samplingOperator)

    samplingStandard = etree.SubElement(
        fieldResearch,
        _garcom("samplingStandard"),
        attrib={"codeSpace": "urn:bro:gar:SamplingStandard"},
    )
    samplingStandard.text = str(field_research["samplingStandard"])

    samplingDevice = etree.SubElement(fieldResearch, _garcom("samplingDevice"))
    pumpType = etree.SubElement(
        samplingDevice, _garcom("pumpType"), attrib={"codeSpace": "urn:bro:gar:PumpType"}
    )
    pumpType.text = str(field_research["pumpType"])

    fieldObservation = etree.SubElement(fieldResearch, _garcom("fieldObservation"))

    if field_research.get("primaryColour"):
        primaryColour = etree.SubElement(
            fieldObservation,
            _garcom("primaryColour"),
            attrib={"codeSpace": "urn:bro:gar:Colour"},
        )
        primaryColour.text = str(field_research["primaryColour"])

    if field_research.get("secondaryColour"):
        secondaryColour = etree.SubElement(
            fieldObservation,
            _garcom("secondaryColour"),
            attrib={"codeSpace": "urn:bro:gar:Colour"},
        )
        secondaryColour.text = str(field_research["secondaryColour"])

    if field_research.get("colourStrength"):
        colourStrength = etree.SubElement(
            fieldObservation,
            _garcom("colourStrength"),
            attrib={"codeSpace": "urn:bro:gar:ColourStrength"},
        )
        colourStrength.text = str(field_research["colourStrength"])

    boolean_fields = [
        "abnormalityInCooling",
        "abnormalityInDevice",
        "pollutedByEngine",
        "filterAerated",
        "groundWaterLevelDroppedTooMuch",
        "abnormalFilter",
        "sampleAerated",
        "hoseReused",
        "temperatureDifficultToMeasure",
    ]
    for field in boolean_fields:
        element = etree.SubElement(fieldObservation, _garcom(field))
        element.text = str(field_research[field])

    for measurement in field_research.get("fieldMeasurements", []):
        fieldResearch.append(gen_field_measurement(measurement))

    return fieldResearch


def gen_analysis(analysis: dict) -> etree.Element:
    garAnalysis = etree.Element(_garcom("analysis"))

    parameter = etree.SubElement(garAnalysis, _garcom("parameter"))
    parameter.text = str(analysis["parameter"])

    if analysis.get("analysisMeasurementValue") is not None:
        analysisMeasurementValue = etree.SubElement(
            garAnalysis,
            _garcom("analysisMeasurementValue"),
            attrib={"uom": str(analysis.get("unit", ""))},
        )
        analysisMeasurementValue.text = str(analysis["analysisMeasurementValue"])
    elif analysis.get("limitSymbol"):
        analysisMeasurementValue = etree.SubElement(
            garAnalysis, _garcom("analysisMeasurementValue")
        )
        _set_nil(analysisMeasurementValue)

    if analysis.get("limitSymbol"):
        limitSymbol = etree.SubElement(
            garAnalysis,
            _garcom("limitSymbol"),
            attrib={"codeSpace": "urn:bro:gar:LimitSymbol"},
        )
        limitSymbol.text = str(analysis["limitSymbol"])

    if analysis.get("reportingLimit") is not None:
        reportingLimit = etree.SubElement(
            garAnalysis,
            _garcom("reportingLimit"),
            attrib={"uom": str(analysis.get("unit", ""))},
        )
        reportingLimit.text = str(analysis["reportingLimit"])

    qualityControlStatus = etree.SubElement(
        garAnalysis,
        _garcom("qualityControlStatus"),
        attrib={"codeSpace": "urn:bro:gar:QualityControlStatus"},
    )
    qualityControlStatus.text = str(analysis["qualityControlStatus"])

    return garAnalysis


def gen_analysis_process(process: dict) -> etree.Element:
    analysisProcess = etree.Element(_garcom("analysisProcess"))

    analysisDate = etree.SubElement(analysisProcess, _garcom("analysisDate"))
    if process.get("date"):
        date = etree.SubElement(analysisDate, f"{{{BROCOM}}}date")
        date.text = str(process["date"])
    else:
        _set_nil(analysisDate)

    analyticalTechnique = etree.SubElement(
        analysisProcess, _garcom("analyticalTechnique")
    )
    if process.get("analyticalTechnique"):
        analyticalTechnique.set("codeSpace", "urn:bro:gar:AnalyticalTechnique")
        analyticalTechnique.text = str(process["analyticalTechnique"])
    else:
        _set_nil(analyticalTechnique)

    valuationMethod = etree.SubElement(analysisProcess, _garcom("valuationMethod"))
    if process.get("valuationMethod"):
        valuationMethod.set("codeSpace", "urn:bro:gar:ValuationMethod")
        valuationMethod.text = str(process["valuationMethod"])
    else:
        _set_nil(valuationMethod)

    for analysis in process.get("analyses", []):
        analysisProcess.append(gen_analysis(analysis))

    return analysisProcess


def gen_laboratory_analysis(lab_analysis: dict) -> etree.Element:
    laboratoryAnalysis = etree.Element("laboratoryAnalysis")

    responsibleLaboratory = etree.SubElement(
        laboratoryAnalysis, _garcom("responsibleLaboratory")
    )
    if lab_analysis.get("responsibleLaboratoryKvk"):
        chamberOfCommerceNumber = etree.SubElement(
            responsibleLaboratory, f"{{{BROCOM}}}chamberOfCommerceNumber"
        )
        chamberOfCommerceNumber.text = str(lab_analysis["responsibleLaboratoryKvk"])
    else:
        _set_nil(responsibleLaboratory)

    for process in lab_analysis.get("analysisProcesses", []):
        laboratoryAnalysis.append(gen_analysis_process(process))

    return laboratoryAnalysis
