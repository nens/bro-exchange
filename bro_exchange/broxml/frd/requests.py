from lxml import etree
from abc import ABC, abstractmethod

import bro_exchange.broxml.frd.constructables as constructables
from bro_exchange.broxml.mappings import frd_namespaces
from . import namespaces


class FRDRequest(ABC):
    def __init__(self, metadata: dict, srcdocdata: dict) -> None:
        self.request_type = None
        self.namespace = None
        self.xsi_schema_location = None
        self.metadata = metadata
        self.srcdocdata = srcdocdata
        self.xml_tree = None
        self.source_document = None
        self.id_count = 1

    def generate_xml_file(self):
        """ Generates the XML file, based on the provide sourcedocsdata
        """
        self.setup_xml_tree()
        self.add_metadata()

        self.source_document = etree.Element("sourceDocument")
        self.create_sourcedocument()
        self.xml_tree.append(self.source_document)

        self.xml_tree = etree.ElementTree(self.xml_tree)

        return self.xml_tree

    def setup_xml_tree(self):
        """ Sets up the basis of a startregistration xml file, consisting of the namespace urls."""
        self.xml_tree = etree.Element(
            self.request_type,
            nsmap=self.namespace,
        )

        if self.xsi_schema_location:
            self.xml_tree.set(
                "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
                self.xsi_schema_location,
            )

    def add_metadata(self):
        """ Fills in the metadata: all information between the namespace links and the sourcedocs."""

        if "request_reference" in self.metadata:
            request_reference = etree.SubElement(
                self.xml_tree,
                ("{%s}" % frd_namespaces["brocom"]) + "requestReference",
            )
            request_reference.text = self.metadata["request_reference"]

        if "delivery_accountable_party" in self.metadata:
            delivery_accountable_party = etree.SubElement(
                self.xml_tree,
                ("{%s}" % frd_namespaces["brocom"]) + "deliveryAccountableParty",
            )
            delivery_accountable_party.text = self.metadata[
                "delivery_accountable_party"
            ]

        if "bro_id" in self.metadata:
            bro_id = etree.SubElement(
                self.xml_tree,
                ("{%s}" % frd_namespaces["brocom"]) + "broId",
            )
            bro_id.text = self.metadata["bro_id"]

        if "quality_regime" in self.metadata:
            quality_regime = etree.SubElement(
                self.xml_tree,
                ("{%s}" % frd_namespaces["brocom"]) + "qualityRegime",
            )
            quality_regime.text = self.metadata["quality_regime"]

        if "date_to_be_corrected" in self.metadata:
            date_tobe_corrected_element = etree.SubElement(
                self.xml_tree,
                "dateToBeCorrected",
            )
            date_tobe_corrected_element.text = self.metadata["date_to_be_corrected"]

        if "correction_reason" in self.metadata:
            bro_id = etree.SubElement(
                self.xml_tree,
                "correctionReason",
                attrib={"codeSpace": "urn:bro:frd:CorrectionReason"},
            )
            bro_id.text = self.metadata["correction_reason"]

    @abstractmethod
    def create_sourcedocument(self):
        """Creates the sourcedocs XML structure."""
        pass


class FRDStartRegistrationTool(FRDRequest):
    """ Handles the requests for startregistration of a FRD.
    
    Options are:
        - Registration
        - Replace
    """

    def __init__(self, metadata: dict, srcdocdata: dict, request_type: str) -> None:
        super().__init__(metadata, srcdocdata)
        self.request_type = request_type
        self.namespace = namespaces.namespace[f"FRD_{self.request_type}"]
        self.xsi_schema_location = namespaces.xsi_schemalocation

    def create_sourcedocument(self):

        # Create Startregistration element
        frd_startregistration = etree.Element(
            "{http://www.broservices.nl/xsd/isfrd/1.0}FRD_StartRegistration"
        )
        frd_startregistration.set(
            "{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}"
        )
        self.id_count += 1

        # Add object id accountable party subelement to frd_startregistration
        object_id_accountable_party = etree.SubElement(
            frd_startregistration,
            "{http://www.broservices.nl/xsd/isfrd/1.0}objectIdAccountableParty",
        )
        object_id_accountable_party.text = self.srcdocdata[
            "object_id_accountable_party"
        ]

        # Check if gmn is present in srcdocdata. If so, create element
        if self.srcdocdata["gmn_bro_id"] is not None:
            for gmn_bro_id in self.srcdocdata["gmn_bro_id"]
                grounwater_monitoring_net = etree.Element("groundwaterMonitoringNet")
                gmn_element = etree.SubElement(
                    grounwater_monitoring_net,
                    "{http://www.broservices.nl/xsd/isfrd/1.0}GroundwaterMonitoringNet",
                )
                gmn_element.set(
                    "{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}"
                )
                self.id_count += 1
                gmn_bro_id = etree.SubElement(
                    gmn_element, "{http://www.broservices.nl/xsd/isfrd/1.0}broId"
                )
                gmn_bro_id.text = gmn_bro_id
                frd_startregistration.append(grounwater_monitoring_net)

        # add grounwaterMonitoringTube
        grounwater_monitoring_tube = etree.Element("groundwaterMonitoringTube")
        tube_element = etree.SubElement(
            grounwater_monitoring_tube,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}MonitoringTube",
        )
        tube_element.set("{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}")
        self.id_count += 1

        tube_bro_id = etree.SubElement(
            tube_element, "{http://www.broservices.nl/xsd/frdcommon/1.0}broId"
        )
        tube_bro_id.text = self.srcdocdata["gmw_bro_id"]

        tube_number = etree.SubElement(
            tube_element, "{http://www.broservices.nl/xsd/frdcommon/1.0}tubeNumber"
        )
        tube_number.text = self.srcdocdata["gmw_tube_number"]

        frd_startregistration.append(grounwater_monitoring_tube)

        # Add startregistration to sourcedocs
        self.source_document.append(frd_startregistration)


class GEMConfigurationTool(FRDRequest):
    """ Handles the requests for GEM Configurations.
    
    Options are:
        - Registration
        - Replace
        - Delete
    """

    def __init__(
        self, metadata: dict = None, srcdocdata: dict = None, request_type: str = None
    ):
        super().__init__(metadata, srcdocdata)
        self.request_type = request_type
        self.namespace = namespaces.namespace[
            f"FRD_GEM_Configuration_{self.request_type}"
        ]
        self.xsi_schema_location = namespaces.xsi_schemalocation

    def create_sourcedocument(self):

        # Create Main element
        gem_measurement_configuration = etree.Element(
            "FRD_GEM_MeasurementConfiguration"
        )
        gem_measurement_configuration.set(
            "{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}"
        )

        self.id_count += 1

        for configuration in self.srcdocdata["measurement_configurations"]:
            gem_measurement_configuration.append(
                constructables.measurement_configuration(configuration)
            )

        self.source_document.append(gem_measurement_configuration)


class FRDClosureTool(FRDRequest):
    """ Handles the requests for Closures of a FRD.
    
    Options are:
        - Registration
        - Delete
    """

    def __init__(
        self, metadata: dict = None, srcdocdata: dict = None, request_type: str = None
    ) -> None:
        super().__init__(metadata, srcdocdata)
        self.request_type = request_type
        self.namespace = namespaces.namespace[f"FRD_Closure_{self.request_type}"]
        self.xsi_schema_location = namespaces.xsi_schemalocation

    def create_sourcedocument(self):
        frd_closure = etree.Element(
            "{http://www.broservices.nl/xsd/isfrd/1.0}FRD_Closure"
        )
        frd_closure.set("{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}")
        self.source_document.append(frd_closure)


class GEMMeasurementTool(FRDRequest):
    """ Handles the requests for GEM Measurements of a FRD.
    
    Options are:
        - Registration
        - Replace
        - Insert
        - Move
        - Delete
    """
    def __init__(
        self, metadata: dict = None, srcdocdata: dict = None, request_type: str = None
    ) -> None:
        super().__init__(metadata, srcdocdata)
        self.request_type = request_type
        self.namespace = namespaces.namespace[f"FRD_GEM_Measurement_{self.request_type}"]
        self.xsi_schema_location = namespaces.xsi_schemalocation

    def create_sourcedocument(self):
        # Create Main element
        gem_measurement = etree.Element(
            "FRD_GEM_Measurement"
        )
        gem_measurement.set(
            "{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}"
        )
        self.id_count += 1

        # Add relatedGeoElectricMeasurement obj
        related_geo_measurement = etree.SubElement(
            gem_measurement,
            "relatedGeoElectricMeasurement",
        )

        # Add GeoElectricMeasurement  obj
        geo_electric_measurement = etree.SubElement(
            related_geo_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}GeoElectricMeasurement",
        )

        geo_electric_measurement.set(
            "{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}"
        )
        self.id_count += 1

        # Add measurement date element
        measurement_date = etree.SubElement(
            geo_electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}measurementDate",
        )

        measurement_date.text = self.srcdocdata["measurement_date"]

        # Add measurement operator element
        measurement_operator = etree.SubElement(
            geo_electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}measurementOperator",
        )

        measurement_operator_kvk = etree.SubElement(
            measurement_operator,
            "{http://www.broservices.nl/xsd/brocommon/3.0}chamberOfCommerceNumber",
        )

        measurement_operator_kvk.text = self.srcdocdata["measuring_responsible_party"]

        # Add determination procedure element
        determination_procedure  = etree.SubElement(
            geo_electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}determinationProcedure",
            attrib={"codeSpace": "urn:bro:frd:DeterminationProcedure"},
        )

        determination_procedure.text = self.srcdocdata["measuring_procedure"]


        # Add evaluation procedure element
        evaluation_procedure  = etree.SubElement(
            geo_electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}evaluationProcedure",
            attrib={"codeSpace": "urn:bro:frd:EvaluationProcedure"},
        )

        evaluation_procedure.text = self.srcdocdata["evaluation_procedure"]

        # Add measure elements
        for measure in self.srcdocdata["measurements"]:
            constructables.add_measure_element(measure=measure, parent=geo_electric_measurement)
           
        # Add evaluation procedure element
        related_calculated_apparent_element  = etree.SubElement(
            geo_electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}relatedCalculatedApparentFormationResistance",
        )

        related_calculated_apparent_subelement  = etree.SubElement(
            related_calculated_apparent_element,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}CalculatedApparentFormationResistance",
        )

        related_calculated_apparent_subelement.set(
            "{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}"
        )
        self.id_count += 1

        # add calculation operator element
        calculation_operator_element  = etree.SubElement(
            related_calculated_apparent_subelement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}calculationOperator",
        )

        calculation_operator_kvk_element  = etree.SubElement(
            calculation_operator_element,
            "{http://www.broservices.nl/xsd/brocommon/3.0}chamberOfCommerceNumber",
        )

        calculation_operator_kvk_element.text = self.srcdocdata["calculated_method_responsible_party"]

        # Add evaluation procedure element
        evaluation_procedure_element  = etree.SubElement(
            related_calculated_apparent_subelement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}evaluationProcedure",
            attrib={"codeSpace": "urn:bro:frd:EvaluationProcedure"},
        )

        evaluation_procedure_element.text = self.srcdocdata["calculated_method_procedure"]

        # add series element
        series_element  = etree.SubElement(
            related_calculated_apparent_subelement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}apparentFormationResistanceSeries",
        )

        # Add dataArray element
        data_array_element = etree.SubElement(
            series_element,
            "{http://www.opengis.net/swe/2.0}DataArray",
        )

        data_array_element.set(
            "id", f"id_000{self.id_count}"
        )
        self.id_count += 1

        # add element count
        element_count_element = etree.SubElement(
            data_array_element,
            "{http://www.opengis.net/swe/2.0}elementCount",
        )

        count_element = etree.SubElement(
            element_count_element,
            "{http://www.opengis.net/swe/2.0}Count",
        )

        value_element = etree.SubElement(
            count_element,
            "{http://www.opengis.net/swe/2.0}value",
        )

        value_element.text = str(self.srcdocdata["measurement_count"])

        # add element type element
        etree.SubElement(
            data_array_element,
            "{http://www.opengis.net/swe/2.0}elementType",
            attrib={
                "name": "SchijnbareFormatieweerstandRecord",
                "{http://www.w3.org/1999/xlink}href":"https://schema.broservices.nl/xsd/frdcommon/1.0/ApparentFormationResistanceRecord.xml",
                },
        )

        # add encoding
        encoding_element = etree.SubElement(
            data_array_element,
            "{http://www.opengis.net/swe/2.0}encoding",
        )

        etree.SubElement(
            encoding_element,
            "{http://www.opengis.net/swe/2.0}TextEncoding",
            attrib={
                "collapseWhiteSpaces": "true",
                "decimalSeparator":".",
                "tokenSeparator":",",
                "blockSeparator":" ",
                },
        )

        # add values
        values_element = etree.SubElement(
            data_array_element,
            "{http://www.opengis.net/swe/2.0}values",
        )

        values_element.text = self.srcdocdata["calculated_values"]

        # add to sourcedocs
        self.source_document.append(gem_measurement)
    
 
class EMMConfigurationTool(FRDRequest):
    """ Handles the requests for GEM Configurations.
    
    Options are:
        - Registration
        - Replace
        - Delete
    """

    def __init__(
        self, metadata: dict = None, srcdocdata: dict = None, request_type: str = None
    ):
        super().__init__(metadata, srcdocdata)
        self.request_type = request_type
        self.namespace = namespaces.namespace[
            f"FRD_EMM_InstrumentConfiguration_{self.request_type}"
        ]
        self.xsi_schema_location = namespaces.xsi_schemalocation

    def create_sourcedocument(self):

        # Create Main element
        gem_measurement_configuration = etree.Element(
            "FRD_EMM_InstrumentConfiguration"
        )
        gem_measurement_configuration.set(
            "{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}"
        )
        self.id_count += 1

        # create maininstrument configuration element
        instrument_configuration_main_element = etree.SubElement(
            gem_measurement_configuration,
            "instrumentConfiguration",
        )

        # Create sub instrument configuration element
        instrument_congonfiguration_sub_element = etree.SubElement(
            instrument_configuration_main_element,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}InstrumentConfiguration",
        )
        instrument_congonfiguration_sub_element.set(
            "{http://www.opengis.net/gml/3.2}id", self.srcdocdata['instrument_configuration_id']
        )


        # create instrumentConfigurationID element
        config_id_element = etree.SubElement(
            instrument_congonfiguration_sub_element,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}instrumentConfigurationID",
        )
        config_id_element.text = str(self.srcdocdata['instrument_configuration_id'])


        # create relativePositionTransmitterCoil element
        transmitter_element = etree.SubElement(
            instrument_congonfiguration_sub_element,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}relativePositionTransmitterCoil",
            attrib={"uom": "cm"},
        )
        transmitter_element.text = str(self.srcdocdata['relative_position_transmitter_coil'])

        # create relativePositionPrimaryReceiverCoil element
        primary_coil_element = etree.SubElement(
            instrument_congonfiguration_sub_element,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}relativePositionPrimaryReceiverCoil",
            attrib={"uom": "cm"},
        )
        primary_coil_element.text = str(self.srcdocdata['relative_position_primary_receiver_coil'])


        # create secondaryReceiverCoilAvailable element
        secondary_coil_element = etree.SubElement(
            instrument_congonfiguration_sub_element,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}secondaryReceiverCoilAvailable",
        )
        secondary_coil_element.text = str(self.srcdocdata['secondary_receiver_coil_available'])

        if "relative_position_secondary_receiver_coil" in self.srcdocdata:
            # create relativePositionPrimaryReceiverCoil element
            secondary_coil_position_element = etree.SubElement(
                instrument_congonfiguration_sub_element,
                "{http://www.broservices.nl/xsd/frdcommon/1.0}relativePositionSecondaryReceiverCoil",
                attrib={"uom": "cm"},
            )
            secondary_coil_position_element.text = str(self.srcdocdata['relative_position_secondary_receiver_coil'])

        # create coilFrequencyKnown element
        coil_frequency_present_element = etree.SubElement(
            instrument_congonfiguration_sub_element,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}coilFrequencyKnown",
        )
        coil_frequency_present_element.text = str(self.srcdocdata['coil_frequency_known'])

        if "coilfrequency" in self.srcdocdata:
            # create relativePositionPrimaryReceiverCoil element
            coil_frequency_element = etree.SubElement(
                instrument_congonfiguration_sub_element,
                "{http://www.broservices.nl/xsd/frdcommon/1.0}coilFrequency",
                attrib={"uom": "kHz"},
            )
            coil_frequency_element.text = str(self.srcdocdata['coilfrequency'])

        # create instrumentLength element
        instrument_length_element = etree.SubElement(
            instrument_congonfiguration_sub_element,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}instrumentLength",
            attrib={"uom": "cm"},
        )
        instrument_length_element.text = str(self.srcdocdata['instrument_length'])

        self.source_document.append(gem_measurement_configuration)

class EMMMeasurementTool(FRDRequest):
    """ Handles the requests for EMM Measurements.
    
    Options are:
        - Registration
        - Replace
        - Insert
        - Move
        - Delete
    """

    def __init__(
        self, metadata: dict = None, srcdocdata: dict = None, request_type: str = None
    ):
        super().__init__(metadata, srcdocdata)
        self.request_type = request_type
        self.namespace = namespaces.namespace[
            f"FRD_EMM_Measurement_{self.request_type}"
        ]
        self.xsi_schema_location = namespaces.xsi_schemalocation

    def create_sourcedocument(self):
        # Create Main element
        emm_measurement = etree.Element(
            "FRD_EMM_Measurement"
        )
        emm_measurement.set(
            "{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}"
        )
        self.id_count += 1

        # Add relatedElectromagneticMeasurement obj
        related_electro_measurement = etree.SubElement(
            emm_measurement,
            "relatedElectromagneticMeasurement",
        )

        # Add GeoElectricMeasurement  obj
        electric_measurement = etree.SubElement(
            related_electro_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}ElectromagneticMeasurement",
        )

        electric_measurement.set(
            "{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}"
        )
        self.id_count += 1

        # Add measurement date element
        measurement_date = etree.SubElement(
            electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}measurementDate",
        )

        measurement_date.text = str(self.srcdocdata["measurement_date"])

        # Add measurement operator element
        measurement_operator = etree.SubElement(
            electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}measurementOperator",
        )

        measurement_operator_kvk = etree.SubElement(
            measurement_operator,
            "{http://www.broservices.nl/xsd/brocommon/3.0}chamberOfCommerceNumber",
        )

        measurement_operator_kvk.text = str(self.srcdocdata["measuring_responsible_party"])

        # Add determination procedure element
        determination_procedure  = etree.SubElement(
            electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}determinationProcedure",
            attrib={"codeSpace": "urn:bro:frd:DeterminationProcedure"},
        )

        determination_procedure.text = self.srcdocdata["measuring_procedure"]

        # Add evaluation procedure element
        evaluation_procedure  = etree.SubElement(
            electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}evaluationProcedure",
            attrib={"codeSpace": "urn:bro:frd:EvaluationProcedure"},
        )

        evaluation_procedure.text = str(self.srcdocdata["evaluation_procedure"])

        # add measuremetn series element
        measurement_series  = etree.SubElement(
            electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}measurementSeries",
        )

        data_array = etree.SubElement(
            measurement_series,
            "{http://www.opengis.net/swe/2.0}DataArray",
        )

        data_array.set(
            "id", f"id_000{self.id_count}"
        )
        self.id_count += 1

        # Add element count
        element_count  = etree.SubElement(
            data_array,
            "{http://www.opengis.net/swe/2.0}elementCount",
        )

        count = etree.SubElement(
            element_count,
            "{http://www.opengis.net/swe/2.0}Count",
        )

        value = etree.SubElement(
            count,
            "{http://www.opengis.net/swe/2.0}value",
        )

        value.text = str(self.srcdocdata["element_count"])

        # add element type element
        etree.SubElement(
            data_array,
            "{http://www.opengis.net/swe/2.0}elementType",
            attrib={
                "name": "ElektromagnetischeMetingRecord",
                "{http://www.w3.org/1999/xlink}href":"https://schema.broservices.nl/xsd/frdcommon/1.0/ElectromagneticMeasurementRecord.xml",
                },
        )

        # add encoding
        encoding_element = etree.SubElement(
            data_array,
            "{http://www.opengis.net/swe/2.0}encoding",
        )

        etree.SubElement(
            encoding_element,
            "{http://www.opengis.net/swe/2.0}TextEncoding",
            attrib={
                "collapseWhiteSpaces": "true",
                "decimalSeparator":".",
                "tokenSeparator":",",
                "blockSeparator":" ",
                },
        )

        # add values
        values_element = etree.SubElement(
            data_array,
            "{http://www.opengis.net/swe/2.0}values",
        )

        values_element.text = str(self.srcdocdata["measurement_data"])

        # add relatedInstrumentConfiguration element
        etree.SubElement(
            electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}relatedInstrumentConfiguration",
            attrib={
                "{http://www.w3.org/1999/xlink}href":str(self.srcdocdata["related_instrument_config"],)
                },
        )

        # add relatedCalculatedApparentFormationResistance element
        related_calc_form_res  = etree.SubElement(
            electric_measurement,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}relatedCalculatedApparentFormationResistance",
        )

        calc_form_res = etree.SubElement(
            related_calc_form_res,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}CalculatedApparentFormationResistance",
        )

        calc_form_res.set(
            "{http://www.opengis.net/gml/3.2}id", f"id_000{self.id_count}"
        )
        self.id_count += 1


        # Add measurement operator element
        calculation_operator = etree.SubElement(
            calc_form_res,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}calculationOperator",
        )

        calculation_operator_kvk = etree.SubElement(
            calculation_operator,
            "{http://www.broservices.nl/xsd/brocommon/3.0}chamberOfCommerceNumber",
        )

        calculation_operator_kvk.text = str(self.srcdocdata["calculated_measurement_operator"])

        # Add evaluation procedure element
        evaluation_procedure  = etree.SubElement(
            calc_form_res,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}evaluationProcedure",
            attrib={"codeSpace": "urn:bro:frd:EvaluationProcedure"},
        )

        evaluation_procedure.text = str(self.srcdocdata["calculated_determination_procedure"])

        ############


        # add apparentFormationResistanceSeries
        apparent_series  = etree.SubElement(
            calc_form_res,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}apparentFormationResistanceSeries",
        )

        data_array2 = etree.SubElement(
            apparent_series,
            "{http://www.opengis.net/swe/2.0}DataArray",
        )

        data_array2.set(
            "id", f"id_000{self.id_count}"
        )
        self.id_count += 1

        # Add element count
        element_count  = etree.SubElement(
            data_array2,
            "{http://www.opengis.net/swe/2.0}elementCount",
        )

        count = etree.SubElement(
            element_count,
            "{http://www.opengis.net/swe/2.0}Count",
        )

        value = etree.SubElement(
            count,
            "{http://www.opengis.net/swe/2.0}value",
        )

        value.text = str(self.srcdocdata["formation_measurement_data_count"])

        # add element type element
        etree.SubElement(
            data_array2,
            "{http://www.opengis.net/swe/2.0}elementType",
            attrib={
                "name": "SchijnbareFormatieweerstandRecord",
                "{http://www.w3.org/1999/xlink}href":"https://schema.broservices.nl/xsd/frdcommon/1.0/ApparentFormationResistanceRecord.xml",
                },
        )

        # add encoding
        encoding_element = etree.SubElement(
            data_array2,
            "{http://www.opengis.net/swe/2.0}encoding",
        )

        etree.SubElement(
            encoding_element,
            "{http://www.opengis.net/swe/2.0}TextEncoding",
            attrib={
                "collapseWhiteSpaces": "true",
                "decimalSeparator":".",
                "tokenSeparator":",",
                "blockSeparator":" ",
                },
        )

        # add values
        values_element = etree.SubElement(
            data_array2,
            "{http://www.opengis.net/swe/2.0}values",
        )

        values_element.text = str(self.srcdocdata["formation_measurement_data"])

        self.source_document.append(emm_measurement)
