from lxml import etree

from bro_exchange.broxml.mappings import (
    frd_namespaces,
)

class FrdStartregistrationTool:
    """
    Handles all actions for the delivery of FRD Data to the BRO.
    Consists of methods to generate, validate and send FRD XML documents.
    """

    def __init__(self, srcdocdata):
        self.srcdocdata = srcdocdata
    
    def generate_xml_file(self):
        """
        Generates the XML file, based on the provide sourcedocsdata
        """
        self.setup_xml_tree()
        self.fill_sourcedocs()
        
        print(etree.tostring(self.xml_tree, pretty_print=True, encoding="unicode"))

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


    def fill_sourcedocs(self):
        pass