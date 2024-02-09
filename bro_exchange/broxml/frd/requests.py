from lxml import etree
from abc import ABC, abstractmethod

import bro_exchange.broxml.frd.constructables as constructables
from bro_exchange.broxml.mappings import frd_namespaces, frd_nsmap
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
            gmn_bro_id.text = self.srcdocdata["gmn_bro_id"]
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
    def create_sourcedocument(self):
        pass
    