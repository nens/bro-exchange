# =============================================================================
# GMW
# =============================================================================

# %% ns_mappings

ns_regreq_map_gmw1 = {
    "ns": "http://www.broservices.nl/xsd/isgmw/1.1",
    "ns1": "http://www.broservices.nl/xsd/brocommon/3.0",
    "ns2": "http://www.broservices.nl/xsd/gmwcommon/1.1",
    "ns3": "http://www.opengis.net/gml/3.2",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

# %% attribute mappings

codespace_map_gmw1 = {
    "deliveryContext": "urn:bro:gmw:DeliveryContext",
    "constructionStandard": "urn:bro:gmw:ConstructionStandard",
    "initialFunction": "urn:bro:gmw:InitialFunction",
    "wellHeadProtector": "urn:bro:gmw:WellHeadProtector",
    "horizontalPositioningMethod": "urn:bro:gmw:HorizontalPositioningMethod",
    "groundLevelPositioningMethod": "urn:bro:gmw:GroundLevelPositioningMethod",
    "tubeType": "urn:bro:gmw:TubeType",
    "tubeStatus": "urn:bro:gmw:TubeStatus",
    "tubeTopPositioningMethod": "urn:bro:gmw:TubeTopPositioningMethod",
    "tubePackingMaterial": "urn:bro:gmw:TubePackingMaterial",
    "tubeMaterial": "urn:bro:gmw:TubeMaterial",
    "glue": "urn:bro:gmw:Glue",
    "sockMaterial": "urn:bro:gmw:SockMaterial",
    "electrodePackingMaterial": "urn:bro:gmw:ElectrodePackingMaterial",
    "electrodeStatus": "urn:bro:gmw:ElectrodeStatus",
    "localVerticalReferencePoint": "urn:bro:gmw:LocalVerticalReferencePoint",
    "wellStability": "urn:bro:gmw:WellStability",
    "correctionReason": "urn:bro:gmw:CorrectionReason",
}


# =============================================================================
# GMN
# =============================================================================

# %% ns_mappings

ns_regreq_map_gmn1 = {"xmlns": "http://www.broservices.nl/xsd/isgmn/1.0"}

ns_regreq_map_gmn2 = {
    "brocom": "http://www.broservices.nl/xsd/brocommon/3.0",
    "gml": "http://www.opengis.net/gml/3.2",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

xsi_regreq_map_gmn1 = {
    "schemaLocation": "http://www.broservices.nl/xsd/isgmn/1.0 https://schema.broservices.nl/xsd/isgmn/1.0/isgmn-messages.xsd"
}

# %% attribute mappings

codespace_map_gmn1 = {
    "deliveryContext": "urn:bro:gmn:DeliveryContext",
    "monitoringPurpose": "urn:bro:gmn:MonitoringPurpose",
    "groundwaterAspect": "urn:bro:gmn:GroundwaterAspect",
    "correctionReason": "urn:bro:gmn:CorrectionReason",
}


# =============================================================================
# GLD
# =============================================================================

# %% ns_mappings

ns_regreq_map_gld1 = {"xmlns": "http://www.broservices.nl/xsd/isgld/1.0"}

ns_regreq_map_gld2 = {
    "brocom": "http://www.broservices.nl/xsd/brocommon/3.0",
    "gldcom": "http://www.broservices.nl/xsd/gldcommon/1.0",
    "gml": "http://www.opengis.net/gml/3.2",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

ns_regreq_map_gld3 = {
    "wml2": "http://www.opengis.net/waterml/2.0",
    "gmd": "http://www.isotc211.org/2005/gmd",
    "gco": "http://www.isotc211.org/2005/gco",
    "om": "http://www.opengis.net/om/2.0",
    "swe": "http://www.opengis.net/swe/2.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "brocom": "http://www.broservices.nl/xsd/brocommon/3.0",
    "gldcom": "http://www.broservices.nl/xsd/gldcommon/1.0",
    "gml": "http://www.opengis.net/gml/3.2",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


xsi_regreq_map_gld1 = {
    "schemaLocation": "http://www.broservices.nl/xsd/isgld/1.0 https://schema.broservices.nl/xsd/isgld/1.0/isgld-messages.xsd"
}

# %% attribute mappings

codespace_map_gld1 = {
    "codeList": "urn:ISO:19115:CI_RoleCode",
    "principalInvestigator": "urn:bro:gld:ObservationMetadata:principalInvestigator",
    "observationType": "urn:bro:gld:ObservationMetadata:observationType",
    "ObservationType": "urn:bro:gld:ObservationType",
    "StatusCode": "urn:bro:gld:StatusCode",
    "airPressureCompensationType": "urn:bro:gld:ObservationProcess:airPressureCompensationType",
    "AirPressureCompensationType": "urn:bro:gld:AirPressureCompensationType",
    "evaluationProcedure": "urn:bro:gld:ObservationProcess:evaluationProcedure",
    "EvaluationProcedure": "urn:bro:gld:EvaluationProcedure",
    "measurementInstrumentType": "urn:bro:gld:ObservationProcess:measurementInstrumentType",
    "MeasurementInstrumentType": "urn:bro:gld:MeasurementInstrumentType",
    "ProcessReference": "urn:bro:gld:ProcessReference",
    "StatusQualityControl": "urn:bro:gld:StatusQualityControl",
    "censoringLimitvalue": "urn:bro:gld:PointMetadata:censoringLimitvalue",
}
