from lxml import etree

from bro_exchange.broxml.mappings import (
    frd_namespaces,
    frd_nsmap
)

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

