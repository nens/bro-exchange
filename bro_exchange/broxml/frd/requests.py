from lxml import etree

from bro_exchange.broxml.mappings import (
    frd_namespaces,
    frd_nsmap
)

def add_electrode(element, electrode_number):
    """
    Adds an electrode subelement to an existing element
    """
    element_str = "{http://www.broservices.nl/xsd/frdcommon/1.0}electrode"
    element_str = element_str + str(electrode_number)
    subelement = etree.SubElement(
            element,
            element_str,
        )
    
    return subelement


def fill_ellectrode_information(electrode_element, cable_number, electrode_number):
    """
    Takes in the electrode xml element, and fills the xml with the cable/electrode numbers
    """
    cable_number_element = etree.SubElement(
            electrode_element,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}cableNumber",
        )
    cable_number_element.text = str(cable_number)
    electrode_number_element = etree.SubElement(
            electrode_element,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}electrodeNumber",
        )
    electrode_number_element.text = str(electrode_number)

class FrdStartregistrationTool:
    """
    Handles all actions for the delivery of FRD Data to the BRO.
    Consists of methods to generate, validate and send FRD XML documents.
    """

    def __init__(self, srcdocdata):
        self.srcdocdata = srcdocdata
        self.xml_tree = None
        self.source_document = None
    
    def generate_xml_file(self):
        """
        Generates the XML file, based on the provide sourcedocsdata
        """
        self.setup_xml_tree()
        self.create_sourcedocument()

        self.xml_tree.append(self.source_document)

        self.xml_tree = etree.ElementTree(self.xml_tree)
        
        return self.xml_tree

    def setup_xml_tree(self):
        """
        Sets up the basis of a startregistration xml file
        """
        # Setup file
        self.xml_tree = etree.Element(
                "registrationRequest",
                nsmap=frd_namespaces,
            )
        
        self.xml_tree.set(
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
            "http://www.broservices.nl/xsd/isfrd/1.0 ../../XSD/isfrd-messages.xsd",
        )

        # add request
        request_reference = etree.SubElement(
            self.xml_tree,
            ("{%s}" % frd_namespaces["brocom"]) + "requestReference",
            nsmap=frd_namespaces,
        )
        request_reference.text = self.srcdocdata["request_reference"]

        # add delivery accountable party
        delivery_accountable_party = etree.SubElement(
            self.xml_tree,
            ("{%s}" % frd_namespaces["brocom"]) + "deliveryAccountableParty",
            nsmap=frd_namespaces,
        )
        delivery_accountable_party.text = self.srcdocdata["delivery_accountable_party"]

        # add quality regime
        quality_regime = etree.SubElement(
            self.xml_tree,
            ("{%s}" % frd_namespaces["brocom"]) + "qualityRegime",
            nsmap=frd_namespaces,
        )
        quality_regime.text = self.srcdocdata["quality_regime"]


    def create_sourcedocument(self):
        id_count = 1
        self.source_document = etree.Element("sourceDocument", nsmap=frd_nsmap)

        # Create Startregistration element
        frd_startregistration = etree.Element(
            "{http://www.broservices.nl/xsd/isfrd/1.0}FRD_StartRegistration"
        )
        frd_startregistration.set("{http://www.opengis.net/gml/3.2}id", f"id_000{id_count}")
        id_count += 1

        
        # Add object id accountable party subelement to frd_startregistration
        object_id_accountable_party = etree.SubElement(
            frd_startregistration,
            "{http://www.broservices.nl/xsd/isfrd/1.0}objectIdAccountableParty"    
        )
        object_id_accountable_party.text = self.srcdocdata["object_id_accountable_party"]
        

        # Check if gmn is present in srcdocdata. If so, create element
        if self.srcdocdata["gmn_bro_id"] is not None:
            grounwater_monitoring_net = etree.Element("groundwaterMonitoringNet")
            gmn_element = etree.SubElement(
                grounwater_monitoring_net,
                "{http://www.broservices.nl/xsd/frdcommon/1.0}GroundwaterMonitoringNet",
            )
            gmn_element.set("{http://www.opengis.net/gml/3.2}id", f"id_000{id_count}")
            id_count += 1
            gmn_bro_id = etree.SubElement(gmn_element, "{http://www.broservices.nl/xsd/frdcommon/1.0}broId")
            gmn_bro_id.text = self.srcdocdata["gmn_bro_id"]
            frd_startregistration.append(grounwater_monitoring_net)

        # add grounwaterMonitoringTube
        grounwater_monitoring_tube = etree.Element("groundwaterMonitoringTube")
        tube_element = etree.SubElement(
            grounwater_monitoring_tube,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}MonitoringTube",
        )
        tube_element.set("{http://www.opengis.net/gml/3.2}id", f"id_000{id_count}")
        id_count += 1

        tube_bro_id = etree.SubElement(tube_element, "{http://www.broservices.nl/xsd/frdcommon/1.0}broId")
        tube_bro_id.text = self.srcdocdata["gmw_bro_id"]
        
        tube_number = etree.SubElement(tube_element, "{http://www.broservices.nl/xsd/frdcommon/1.0}tubeNumber")
        tube_number.text = self.srcdocdata["gmw_tube_number"]

        frd_startregistration.append(grounwater_monitoring_tube)

        # Add startregistration to sourcedocs
        self.source_document.append(frd_startregistration)


class ConfigurationRegistrationTool:
    """
    Sets up the xml file for the measurement configuration registrations of the FRD domain
    """
    def __init__(self, srcdocdata):
        self.srcdocdata = srcdocdata
        self.xml_tree = None
        self.source_document = None
    
    def generate_xml_file(self):
        """
        Generates the XML file, based on the provide sourcedocsdata
        """
        self.setup_xml_tree()
        self.create_sourcedocument()

        self.xml_tree.append(self.source_document)

        self.xml_tree = etree.ElementTree(self.xml_tree)
        
        return self.xml_tree

    def setup_xml_tree(self):
        """
        Sets up the basis of a startregistration xml file
        """
        
        # Setup file
        self.xml_tree = etree.Element(
                "registrationRequest",
                nsmap=frd_namespaces,
            )
        
        self.xml_tree.set(
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
            "http://www.broservices.nl/xsd/isfrd/1.0 ../../XSD/isfrd-messages.xsd",
        )

        # add request
        request_reference = etree.SubElement(
            self.xml_tree,
            ("{%s}" % frd_namespaces["brocom"]) + "requestReference",
            nsmap=frd_namespaces,
        )
        request_reference.text = self.srcdocdata["request_reference"]


    def create_sourcedocument(self):
        id_count = 1
        self.source_document = etree.Element("sourceDocument", nsmap=frd_nsmap)

        # Create Main element
        gem_measurement_configuration  = etree.Element(
            "FRD_GEM_MeasurementConfiguration"
        )
        gem_measurement_configuration.set("{http://www.opengis.net/gml/3.2}id", f"id_000{id_count}")
        id_count += 1

        
        # Initialize generic measurement configuration element
        measurement_configuration = etree.SubElement(
            gem_measurement_configuration,
            "measurementConfiguration"    
        )

        # Generate actual measurement configuration element
        frd_measurement_configuration = etree.SubElement(
            measurement_configuration,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}MeasurementConfiguration"
        )
        frd_measurement_configuration.set("{http://www.opengis.net/gml/3.2}id", f"{self.srcdocdata['measurement_configuration_id']}")
        

        # Define ID 
        frd_measurement_configuration_id = etree.SubElement(
            frd_measurement_configuration,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}measurementConfigurationID",
        )
        frd_measurement_configuration_id.text = self.srcdocdata["measurement_configuration_id"]


        # Define measurement pair
        measurement_pair = etree.SubElement(
            frd_measurement_configuration,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}measurementPair",
        )

        # Define current pair
        current_pair = etree.SubElement(
            frd_measurement_configuration,
            "{http://www.broservices.nl/xsd/frdcommon/1.0}currentPair",
        )

        # Define electrodes
        mp_electrode1 = add_electrode(measurement_pair, 1)
        mp_electrode2 = add_electrode(measurement_pair, 2)
        cp_electrode1 = add_electrode(current_pair, 1)
        cp_electrode2 = add_electrode(current_pair, 2)

        # Fill electrode information
        fill_ellectrode_information(mp_electrode1, self.srcdocdata["measurement_pair"].elektrode1.cable_number, self.srcdocdata["measurement_pair"].elektrode1.electrode_number)
        fill_ellectrode_information(mp_electrode2, self.srcdocdata["measurement_pair"].elektrode2.cable_number, self.srcdocdata["measurement_pair"].elektrode2.electrode_number)
        fill_ellectrode_information(cp_electrode1, self.srcdocdata["flowcurrent_pair"].elektrode1.cable_number, self.srcdocdata["flowcurrent_pair"].elektrode1.electrode_number)
        fill_ellectrode_information(cp_electrode2, self.srcdocdata["flowcurrent_pair"].elektrode2.cable_number, self.srcdocdata["flowcurrent_pair"].elektrode2.electrode_number)

        self.source_document.append(gem_measurement_configuration)


  


