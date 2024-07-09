import datetime
import pytz
import uuid as uuid_gen

import pandas as pd
from lxml import etree

from bro_exchange.checks import check_missing_args
from bro_exchange.broxml.mappings import (  # mappings
    codespace_map_gld1,
)

# =============================================================================
# General info
# =============================================================================


# %%

# =============================================================================
# Startregistration
# =============================================================================

# %%


def gen_groundwatermonitoringnet(data, net, nsmap, count):
    arglist = {"broId": "obligated"}

    check_missing_args(
        data["groundwaterMonitoringNets"][net],
        arglist,
        f"gen_groundwatermonitoringnet, net with index {str(net)}",
    )

    groundwaterMonitoringNet = etree.Element("groundwaterMonitoringNet")

    GroundwaterMonitoringNet = etree.SubElement(
        groundwaterMonitoringNet,
        ("{%s}" % nsmap["gldcom"]) + "GroundwaterMonitoringNet",
        nsmap=nsmap,
        attrib={("{%s}" % nsmap["gml"]) + "id": f"id_000{str(count)}"},
    )

    count += 1

    broId = etree.SubElement(
        GroundwaterMonitoringNet, ("{%s}" % nsmap["gldcom"]) + "broId", nsmap=nsmap
    )
    broId.text = data["groundwaterMonitoringNets"][net]["broId"]

    return (groundwaterMonitoringNet, count)


# %%


def gen_monitoringpoint(data, point, nsmap, count):
    arglist = {"broId": "obligated", "tubeNumber": "obligated"}

    check_missing_args(
        data["monitoringPoints"][point],
        arglist,
        f"gen_monitoringpoint, point with index {str(point)}",
    )

    monitoringPoint = etree.Element("monitoringPoint")

    GroundwaterMonitoringTube = etree.SubElement(
        monitoringPoint,
        ("{%s}" % nsmap["gldcom"]) + "GroundwaterMonitoringTube",
        nsmap=nsmap,
        attrib={("{%s}" % nsmap["gml"]) + "id": f"id_000{str(count)}"},
    )

    count += 1

    broId = etree.SubElement(
        GroundwaterMonitoringTube, ("{%s}" % nsmap["gldcom"]) + "broId", nsmap=nsmap
    )
    broId.text = data["monitoringPoints"][point]["broId"]

    tubeNumber = etree.SubElement(
        GroundwaterMonitoringTube,
        ("{%s}" % nsmap["gldcom"]) + "tubeNumber",
        nsmap=nsmap,
    )
    tubeNumber.text = str(data["monitoringPoints"][point]["tubeNumber"])

    return (monitoringPoint, count)


# %%

# =============================================================================
# Addition
# =============================================================================

# %%


def gen_metadata_parameters(data, nsmap, codespacemap):
    arglist = {"principalInvestigator": "optional", "observationType": "obligated"}

    check_missing_args(
        data["metadata"]["parameters"], arglist, "gen_metadata_parameters"
    )

    parameterlist = {}

    parameters = list(data["metadata"]["parameters"].keys())

    # principal investigator
    parameterlist["principalInvestigator"] = etree.Element(
        ("{%s}" % nsmap["wml2"]) + "parameter", nsmap=nsmap
    )
    principalInvestigator_namevalue = etree.SubElement(
        parameterlist["principalInvestigator"],
        ("{%s}" % nsmap["om"]) + "NamedValue",
        nsmap=nsmap,
    )
    principalInvestigator_omname = etree.SubElement(
        principalInvestigator_namevalue,
        ("{%s}" % nsmap["om"]) + "name",
        nsmap=nsmap,
        attrib={
            ("{%s}" % nsmap["xlink"]) + "href": codespace_map_gld1[
                "principalInvestigator"
            ]
        },
    )

    principalInvestigator_omvalue = etree.SubElement(
        principalInvestigator_namevalue,
        ("{%s}" % nsmap["om"]) + "value",
        nsmap=nsmap,
        attrib={("{%s}" % nsmap["xsi"]) + "type": "gldcom:OrganizationType"},
    )
    if "principalInvestigator" in parameters:
        if type(data["metadata"]["parameters"]["principalInvestigator"]) != dict:
            chamberOfCommerceNumber = etree.SubElement(
                principalInvestigator_omvalue,
                ("{%s}" % nsmap["gldcom"]) + "chamberOfCommerceNumber",
                nsmap=nsmap,
            )
            chamberOfCommerceNumber.text = str(
                data["metadata"]["parameters"]["principalInvestigator"]
            )
        else:
            if "chamberOfCommerceNumber" in list(
                data["metadata"]["parameters"]["principalInvestigator"].keys()
            ):
                chamberOfCommerceNumber = etree.SubElement(
                    principalInvestigator_omvalue,
                    ("{%s}" % nsmap["gldcom"]) + "chamberOfCommerceNumber",
                    nsmap=nsmap,
                )
                chamberOfCommerceNumber.text = str(
                    data["metadata"]["parameters"]["principalInvestigator"][
                        "chamberOfCommerceNumber"
                    ]
                )
            elif "europeanCompanyRegistrationNumber" in list(
                data["metadata"]["parameters"]["principalInvestigator"].keys()
            ):
                europeanCompanyRegistrationNumber = etree.SubElement(
                    principalInvestigator_omvalue,
                    ("{%s}" % nsmap["gldcom"]) + "europeanCompanyRegistrationNumber",
                    nsmap=nsmap,
                )
                europeanCompanyRegistrationNumber.text = str(
                    data["metadata"]["parameters"]["principalInvestigator"][
                        "europeanCompanyRegistrationNumber"
                    ]
                )

    # observation_type_metadata
    parameterlist["observationType"] = etree.Element(
        ("{%s}" % nsmap["wml2"]) + "parameter", nsmap=nsmap
    )
    observationType_namevalue = etree.SubElement(
        parameterlist["observationType"],
        ("{%s}" % nsmap["om"]) + "NamedValue",
        nsmap=nsmap,
    )
    observationType_omname = etree.SubElement(
        observationType_namevalue,
        ("{%s}" % nsmap["om"]) + "name",
        nsmap=nsmap,
        attrib={
            ("{%s}" % nsmap["xlink"]) + "href": codespace_map_gld1["observationType"]
        },
    )

    observationType_omvalue = etree.SubElement(
        observationType_namevalue,
        ("{%s}" % nsmap["om"]) + "value",
        nsmap=nsmap,
        attrib={
            ("{%s}" % nsmap["xsi"]) + "type": "gml:CodeWithAuthorityType",
            "codeSpace": codespace_map_gld1["ObservationType"],
        },
    )

    observationType_omvalue.text = data["metadata"]["parameters"]["observationType"]

    return parameterlist


# %%


def gen_metadata(data, nsmap, codespacemap):
    arglist = {
        "contact": "optional",  # Defaults to default values, however there are restricted arguments
        "dateStamp": "optional",  # derive it from timeseries
        "identificationInfo": "optional",  # fixed, unknown
        "status": "optional",  # geeft aan of het controle, voorlopige of gevalideerde meting is
        "parameters": "obligated",
    }  # construcatble with restrictions

    check_missing_args(data["metadata"], arglist, "gen_monitoringpoint, metadata")

    metadata = etree.Element(("{%s}" % nsmap["om"]) + "metadata", nsmap=nsmap)

    ObservationMetadata = etree.SubElement(
        metadata, ("{%s}" % nsmap["wml2"]) + "ObservationMetadata", nsmap=nsmap
    )

    # Contact
    contact = etree.SubElement(
        ObservationMetadata, ("{%s}" % nsmap["gmd"]) + "contact", nsmap=nsmap
    )
    CI_ResponsibleParty = etree.SubElement(
        contact, ("{%s}" % nsmap["gmd"]) + "CI_ResponsibleParty", nsmap=nsmap
    )
    organisationName = etree.SubElement(
        CI_ResponsibleParty, ("{%s}" % nsmap["gmd"]) + "organisationName", nsmap=nsmap
    )
    CharacterString = etree.SubElement(
        organisationName, ("{%s}" % nsmap["gco"]) + "CharacterString", nsmap=nsmap
    )
    role = etree.SubElement(
        CI_ResponsibleParty, ("{%s}" % nsmap["gmd"]) + "role", nsmap=nsmap
    )

    if "contact" in data["metadata"].keys():
        CI_RoleCode = etree.SubElement(
            role,
            ("{%s}" % nsmap["gmd"]) + "CI_RoleCode",
            nsmap=nsmap,
            codeList=codespacemap["codeList"],
            codeListValue=data["metadata"]["contact"],
        )
        CI_RoleCode.text = data["metadata"]["contact"]

    else:
        CI_RoleCode = etree.SubElement(
            role,
            ("{%s}" % nsmap["gmd"]) + "CI_RoleCode",
            nsmap=nsmap,
            codeList=codespacemap["codeList"],
            codeListValue="principalInvestigator",
        )
        CI_RoleCode.text = "principalInvestigator "

    # Datestamp:
    dateStamp = etree.SubElement(
        ObservationMetadata, ("{%s}" % nsmap["gmd"]) + "dateStamp", nsmap=nsmap
    )
    Date = etree.SubElement(dateStamp, ("{%s}" % nsmap["gco"]) + "Date", nsmap=nsmap)

    if "dateStamp" in data["metadata"].keys():
        Date.text = data["metadata"]["dateStamp"]
    else:
        Date.text = str(datetime.datetime.now().date())  # Creation Date of Metadata

    # identificationInfo
    if "identificationInfo" in data["metadata"].keys():
        identificationInfo = etree.SubElement(
            ObservationMetadata,
            ("{%s}" % nsmap["gmd"]) + "identificationInfo",
            nsmap=nsmap,
            attrib={
                ("{%s}" % nsmap["gco"]) + "nilReason": data["metadata"][
                    "identificationInfo"
                ]
            },
        )
    else:
        identificationInfo = etree.SubElement(
            ObservationMetadata,
            ("{%s}" % nsmap["gmd"]) + "identificationInfo",
            nsmap=nsmap,
            attrib={("{%s}" % nsmap["gco"]) + "nilReason": "unknown"},
        )
    # status
    if "status" in data["metadata"].keys():
        try:
            if data["metadata"]["parameters"]["observationType"] != "controlemeting":
                status = etree.SubElement(
                    ObservationMetadata,
                    ("{%s}" % nsmap["wml2"]) + "status",
                    nsmap=nsmap,
                    attrib={
                        ("{%s}" % nsmap["xlink"]) + "href": codespace_map_gld1[
                            "StatusCode"
                        ]
                        + ":{}".format(data["metadata"]["status"])
                    },
                )
            else:
                raise Exception(
                    "argument 'status' in observation metadata while 'controlemeting' as observationType: controlemeting \
                                should not have status"
                )
        except:
            raise Exception(
                "argument 'status' in observation metadata while 'controlemeting' as observationType: controlemeting \
                            should not have status"
            )

    else:
        if data["metadata"]["parameters"]["observationType"] != "controlemeting":
            raise Exception(
                "argument 'status' obligated in observation metadata if not'controlemeting' as observationType"
            )

    # restricted parameters
    parameters = gen_metadata_parameters(data, nsmap, codespacemap)
    for param in list(parameters.keys()):
        ObservationMetadata.append(parameters[param])

    return metadata


# %%


def gen_phenomenontime(data, nsmap, codespacemap, count):
    try:
        beginPosition = str(pd.DataFrame(data["result"])["time"][0])[:10]
        endPosition = str(
            pd.DataFrame(data["result"])["time"][len(pd.DataFrame(data["result"])) - 1]
        )
        tz_info = pytz.timezone("Europe/Amsterdam")
        endPosition = datetime.datetime.strptime(endPosition, "%Y-%m-%dT%H:%M:%S%z").astimezone(tz=tz_info)
        endPosition = endPosition.strftime("%Y-%m-%d")
    except:
        raise Exception("Error: phenomenonTime cannot be derived from timeseries")

    phenomenonTime = etree.Element(
        ("{%s}" % nsmap["om"]) + "phenomenonTime", nsmap=nsmap
    )

    TimePeriod = etree.SubElement(
        phenomenonTime,
        ("{%s}" % nsmap["gml"]) + "TimePeriod",
        nsmap=nsmap,
        attrib={("{%s}" % nsmap["gml"]) + "id": f"id_000{str(count)}"},
    )

    count += 1

    beginPosition_ = etree.SubElement(
        TimePeriod, ("{%s}" % nsmap["gml"]) + "beginPosition", nsmap=nsmap
    )
    beginPosition_.text = beginPosition

    endPosition_ = etree.SubElement(
        TimePeriod, ("{%s}" % nsmap["gml"]) + "endPosition", nsmap=nsmap
    )
    endPosition_.text = endPosition

    return (phenomenonTime, count)


# %%


def gen_resulttime(data, nsmap, codespacemap, count):
    # try:

    #     if 'status' in data['metadata'].keys():
    #         if  data['metadata']['status']=='volledigBeoordeeld':
    #             dif = 1

    #         else:
    #             dif = 0
    #     else:
    #         dif = 0

    #     timeseriesdata = pd.DataFrame(data['result'])
    #     timeseriesdata.index=pd.to_datetime(timeseriesdata['time'],format = '%Y-%m-%dT%H:%M:%S')
    #     timeseriesdata['datetime']=timeseriesdata.index
    #     endPosition = str(timeseriesdata['time'][len(timeseriesdata)-1])[:10]

    #     timeposition = str(timeseriesdata['datetime'][len(timeseriesdata)-1]+datetime.timedelta(seconds=dif)).replace(' ','T')  # datumtijd verkrijgen data, automatisch een seconde naar laatste observatie in reeksje

    # except:
    #     raise Exception('Error: resultTime cannot be derived from timeseries')
    timeposition = data["resultTime"]
    resultTime = etree.Element(("{%s}" % nsmap["om"]) + "resultTime", nsmap=nsmap)
    TimeInstant = etree.SubElement(
        resultTime,
        ("{%s}" % nsmap["gml"]) + "TimeInstant",
        nsmap=nsmap,
        attrib={("{%s}" % nsmap["gml"]) + "id": f"id_000{str(count)}"},
    )

    count += 1

    timePosition = etree.SubElement(
        TimeInstant, ("{%s}" % nsmap["gml"]) + "timePosition", nsmap=nsmap
    )
    timePosition.text = timeposition

    return (resultTime, count)


# %%


def gen_procedure_parameters(data, nsmap, codespacemap):
    parameterlist = {}

    parameters = list(data["procedure"]["parameters"].keys())

    # airPressureCompensationType
    if "airPressureCompensationType" in parameters:
        parameterlist["airPressureCompensationType"] = etree.Element(
            ("{%s}" % nsmap["wml2"]) + "parameter", nsmap=nsmap
        )
        airPressureCompensationType_namevalue = etree.SubElement(
            parameterlist["airPressureCompensationType"],
            ("{%s}" % nsmap["om"]) + "NamedValue",
            nsmap=nsmap,
        )

        airPressureCompensationType_name = etree.SubElement(
            airPressureCompensationType_namevalue,
            ("{%s}" % nsmap["om"]) + "name",
            nsmap=nsmap,
            attrib={
                ("{%s}" % nsmap["xlink"]) + "href": codespace_map_gld1[
                    "airPressureCompensationType"
                ]
            },
        )

        airPressureCompensationType_value = etree.SubElement(
            airPressureCompensationType_namevalue,
            ("{%s}" % nsmap["om"]) + "value",
            nsmap=nsmap,
            attrib={
                ("{%s}" % nsmap["xsi"]) + "type": "gml:CodeWithAuthorityType",
                "codeSpace": codespace_map_gld1["AirPressureCompensationType"],
            },
        )

        airPressureCompensationType_value.text = data["procedure"]["parameters"][
            "airPressureCompensationType"
        ]

    # evaluationProcedure
    if "evaluationProcedure" in parameters:
        parameterlist["evaluationProcedure"] = etree.Element(
            ("{%s}" % nsmap["wml2"]) + "parameter", nsmap=nsmap
        )
        evaluationProcedure_namevalue = etree.SubElement(
            parameterlist["evaluationProcedure"],
            ("{%s}" % nsmap["om"]) + "NamedValue",
            nsmap=nsmap,
        )

        evaluationProcedure_name = etree.SubElement(
            evaluationProcedure_namevalue,
            ("{%s}" % nsmap["om"]) + "name",
            nsmap=nsmap,
            attrib={
                ("{%s}" % nsmap["xlink"]) + "href": codespace_map_gld1[
                    "evaluationProcedure"
                ]
            },
        )

        evaluationProcedure_value = etree.SubElement(
            evaluationProcedure_namevalue,
            ("{%s}" % nsmap["om"]) + "value",
            nsmap=nsmap,
            attrib={
                ("{%s}" % nsmap["xsi"]) + "type": "gml:CodeWithAuthorityType",
                "codeSpace": codespace_map_gld1["EvaluationProcedure"],
            },
        )

        evaluationProcedure_value.text = data["procedure"]["parameters"][
            "evaluationProcedure"
        ]

    # measurementInstrumentType
    if "measurementInstrumentType" in parameters:
        parameterlist["measurementInstrumentType"] = etree.Element(
            ("{%s}" % nsmap["wml2"]) + "parameter", nsmap=nsmap
        )
        measurementInstrumentType_namevalue = etree.SubElement(
            parameterlist["measurementInstrumentType"],
            ("{%s}" % nsmap["om"]) + "NamedValue",
            nsmap=nsmap,
        )

        measurementInstrumentType_name = etree.SubElement(
            measurementInstrumentType_namevalue,
            ("{%s}" % nsmap["om"]) + "name",
            nsmap=nsmap,
            attrib={
                ("{%s}" % nsmap["xlink"]) + "href": codespace_map_gld1[
                    "measurementInstrumentType"
                ]
            },
        )

        measurementInstrumentType_value = etree.SubElement(
            measurementInstrumentType_namevalue,
            ("{%s}" % nsmap["om"]) + "value",
            nsmap=nsmap,
            attrib={
                ("{%s}" % nsmap["xsi"]) + "type": "gml:CodeWithAuthorityType",
                "codeSpace": codespace_map_gld1["MeasurementInstrumentType"],
            },
        )

        measurementInstrumentType_value.text = data["procedure"]["parameters"][
            "measurementInstrumentType"
        ]

    return parameterlist


# %%


def gen_procedure(data, nsmap, codespacemap):
    procedure = etree.Element(("{%s}" % nsmap["om"]) + "procedure", nsmap=nsmap)
    ObservationProcess = etree.SubElement(
        procedure,
        ("{%s}" % nsmap["wml2"]) + "ObservationProcess",
        nsmap=nsmap,
        attrib={("{%s}" % nsmap["gml"]) + "id": f"_{uuid_gen.uuid4()}"},
    )
    if "processType" not in data["procedure"].keys():
        processTypestr = "http://www.opengis.net/def/waterml/2.0/processType/Algorithm"
    else:
        processReferencestr = data["procedure"]["processType"]

    processType = etree.SubElement(
        ObservationProcess,
        ("{%s}" % nsmap["wml2"]) + "processType",
        nsmap=nsmap,
        attrib={("{%s}" % nsmap["xlink"]) + "href": processTypestr},
    )
    if "processReference" not in data["procedure"].keys():
        processReferencestr = codespace_map_gld1["ProcessReference"] + ":NEN5120v1991"
    else:
        processReferencestr = (
            codespace_map_gld1["ProcessReference"]
            + ":"
            + data["procedure"]["processReference"]
        )

    processReference = etree.SubElement(
        ObservationProcess,
        ("{%s}" % nsmap["wml2"]) + "processReference",
        nsmap=nsmap,
        attrib={("{%s}" % nsmap["xlink"]) + "href": processReferencestr},
    )

    if "parameters" in data["procedure"].keys():
        # try:
        parameters = gen_procedure_parameters(data, nsmap, codespacemap)
        for param in list(parameters.keys()):
            ObservationProcess.append(parameters[param])
    # except:
    # raise Exception('Error: failed to compile procedure parameters')

    return procedure


# %%


def gen_point_metadata_qualifiers(data, rec, nsmap, codespacemap, count):
    qualifierlist = {}

    metadata = list(rec["metadata"].keys())

    if "StatusQualityControl" in metadata:
        qualifierlist["StatusQualityControl"] = etree.Element(
            ("{%s}" % nsmap["wml2"]) + "qualifier", nsmap=nsmap
        )
        StatusQualityControl_category = etree.SubElement(
            qualifierlist["StatusQualityControl"],
            ("{%s}" % nsmap["swe"]) + "Category",
            nsmap=nsmap,
        )
        StatusQualityControl_codeSpace = etree.SubElement(
            StatusQualityControl_category,
            ("{%s}" % nsmap["swe"]) + "codeSpace",
            nsmap=nsmap,
            attrib={
                ("{%s}" % nsmap["xlink"]) + "href": codespace_map_gld1[
                    "StatusQualityControl"
                ]
            },
        )

        StatusQualityControl_value = etree.SubElement(
            StatusQualityControl_category,
            ("{%s}" % nsmap["swe"]) + "value",
            nsmap=nsmap,
        )
        StatusQualityControl_value.text = str(rec["metadata"]["StatusQualityControl"])

    if "censoringLimitvalue" in metadata:
        qualifierlist["censoringLimitvalue"] = etree.Element(
            ("{%s}" % nsmap["wml2"]) + "qualifier", nsmap=nsmap
        )
        censoringLimitvalue_category = etree.SubElement(
            qualifierlist["censoringLimitvalue"],
            ("{%s}" % nsmap["swe"]) + "Quantity",
            nsmap=nsmap,
            attrib={"definition": codespace_map_gld1["censoringLimitvalue"]},
        )
        censoringLimitvalue_value = etree.SubElement(
            censoringLimitvalue_category,
            ("{%s}" % nsmap["swe"]) + "uom",
            nsmap=nsmap,
            attrib={"code": "m"},
        )

        censoringLimitvalue_value = etree.SubElement(
            censoringLimitvalue_category, ("{%s}" % nsmap["swe"]) + "value", nsmap=nsmap
        )
        censoringLimitvalue_value.text = str(rec["metadata"]["censoringLimitvalue"])

    return qualifierlist


# %%


def gen_point_metadata(data, rec, nsmap, codespacemap, count):
    metadata = etree.Element(("{%s}" % nsmap["wml2"]) + "metadata", nsmap=nsmap)
    TVPMeasurementMetadata = etree.SubElement(
        metadata, ("{%s}" % nsmap["wml2"]) + "TVPMeasurementMetadata", nsmap=nsmap
    )

    if "StatusQualityControl" not in rec["metadata"].keys():
        raise Exception("Error: StatusQualityControl should be in qualifiers")
    if "interpolationType" not in rec["metadata"].keys():
        raise Exception("Error: interpolationType should be in qualifiers")
    else:
        # try:
        qualifiers = gen_point_metadata_qualifiers(
            data, rec, nsmap, codespacemap, count
        )
        for qualifier in list(qualifiers.keys()):
            TVPMeasurementMetadata.append(qualifiers[qualifier])

        if "interpolationType" in rec["metadata"].keys():
            interpolationType = etree.SubElement(
                TVPMeasurementMetadata,
                ("{%s}" % nsmap["wml2"]) + "interpolationType",
                nsmap=nsmap,
                attrib={
                    ("{%s}" % nsmap["xlink"])
                    + "href": "http://www.opengis.net/def/waterml/2.0/interpolationType/{}".format(
                        rec["metadata"]["interpolationType"]
                    )
                },
            )
        if "censoredReason" in rec["metadata"].keys():
            censoredReason = etree.SubElement(
                TVPMeasurementMetadata,
                ("{%s}" % nsmap["wml2"]) + "censoredReason",
                nsmap=nsmap,
                attrib={
                    ("{%s}" % nsmap["xlink"])
                    + "href": "http://www.opengis.net/def/nil/OGC/0/{}".format(
                        rec["metadata"]["censoredReason"]
                    )
                },
            )
    # except:
    # raise Exception('Error: failed to compile point metadata parameters')

    return (metadata, count)


# %%


def gen_point(data, rec, nsmap, codespacemap, count):
    point = etree.Element(("{%s}" % nsmap["wml2"]) + "point", nsmap=nsmap)
    MeasurementTVP = etree.SubElement(
        point, ("{%s}" % nsmap["wml2"]) + "MeasurementTVP", nsmap=nsmap
    )

    time = etree.SubElement(
        MeasurementTVP, ("{%s}" % nsmap["wml2"]) + "time", nsmap=nsmap
    )
    time.text = rec["time"]

    if rec["value"] != "None":
        value = etree.SubElement(
            MeasurementTVP,
            ("{%s}" % nsmap["wml2"]) + "value",
            nsmap=nsmap,
            attrib={"uom": "m"},
        )
        value.text = str(rec["value"])
    else:
        # Note, mogelijk nog aanpassen
        value = etree.SubElement(
            MeasurementTVP,
            ("{%s}" % nsmap["wml2"]) + "value",
            nsmap=nsmap,
            attrib={("{%s}" % nsmap["xsi"]) + "nil": "true"},
        )

    # Generate metadata from qualifiers:
    metadata, count = gen_point_metadata(data, rec, nsmap, codespacemap, count)
    MeasurementTVP.append(metadata)
    return (point, count)


# %%
def gen_result(data, nsmap, codespacemap, count):
    result = etree.Element(("{%s}" % nsmap["om"]) + "result", nsmap=nsmap)
    MeasurementTimeseries = etree.SubElement(
        result,
        ("{%s}" % nsmap["wml2"]) + "MeasurementTimeseries",
        nsmap=nsmap,
        attrib={("{%s}" % nsmap["gml"]) + "id": f"_{uuid_gen.uuid4()}"},
    )

    timeseriesdata = pd.DataFrame(data["result"])
    timeseriesdata.index = range(len(timeseriesdata))

    # Generate points out of timeseriesdata
    points = {}

    for point in range(len(timeseriesdata)):
        points[f"points_{str(point)}"], count = gen_point(
            data, timeseriesdata.iloc[point], nsmap, codespacemap, count
        )
        MeasurementTimeseries.append(points[f"points_{str(point)}"])

    return (result, count)
