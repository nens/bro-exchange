from lxml import etree
from bro_exchange.broxml.mappings import frd_namespaces, frd_nsmap


def electrode(electrode: dict, number: int) -> etree.Element:
    electrode_element = etree.Element(
        "{http://www.broservices.nl/xsd/frdcommon/1.0}electrode" + f"{number}"
    )

    cable_number = etree.SubElement(
        electrode_element, "{http://www.broservices.nl/xsd/frdcommon/1.0}cableNumber"
    )
    cable_number.text = str(electrode["cable_number"])
    electrode_number = etree.SubElement(
        electrode_element,
        "{http://www.broservices.nl/xsd/frdcommon/1.0}electrodeNumber",
    )
    electrode_number.text = str(electrode["electrode_number"])

    return electrode_element


def measurement_pair(measurement_pair: dict) -> etree.Element:
    measurement_pair_element = etree.Element(
        "{http://www.broservices.nl/xsd/frdcommon/1.0}measurementPair"
    )
    measurement_pair_element.append(electrode(measurement_pair["elektrode1"], 1))
    measurement_pair_element.append(electrode(measurement_pair["elektrode2"], 2))
    return measurement_pair_element


def current_pair(current_pair: dict) -> etree.Element:
    current_pair_element = etree.Element(
        "{http://www.broservices.nl/xsd/frdcommon/1.0}currentPair"
    )

    current_pair_element.append(electrode(current_pair["elektrode1"], 1))
    current_pair_element.append(electrode(current_pair["elektrode2"], 2))

    return current_pair_element


def measurement_configuration(measurement_configuration_dict: dict) -> etree.Element:
    measurement_configuration_element = etree.Element(
        "measurementConfiguration",
        nsmap=frd_nsmap,
    )

    measurement_configuration = etree.SubElement(
        measurement_configuration_element,
        "{http://www.broservices.nl/xsd/frdcommon/1.0}MeasurementConfiguration",
    )
    measurement_configuration.set(
        "{http://www.opengis.net/gml/3.2}id",
        f"mc_{measurement_configuration_dict['name']}",
    )
    measurement_configuration_id = etree.SubElement(
        measurement_configuration,
        "{http://www.broservices.nl/xsd/frdcommon/1.0}measurementConfigurationID",
    )
    measurement_configuration_id.text = f"mc_{measurement_configuration_dict['name']}"

    measurement_configuration.append(
        measurement_pair(measurement_configuration_dict["measurement_pair"])
    )
    measurement_configuration.append(
        current_pair(measurement_configuration_dict["flowcurrent_pair"])
    )

    return measurement_configuration_element

def add_measure_element(measure, parent):
    """Creates a measure element for the FRD GEM Measurement"""
    config_name, value = measure


    element = etree.SubElement(
        parent,
        "{http://www.broservices.nl/xsd/frdcommon/1.0}measure",
    )

    resistance_sub_element = etree.SubElement(
        element,
        "{http://www.broservices.nl/xsd/frdcommon/1.0}resistance",
        attrib={"uom": "Ohm"},
    )

    resistance_sub_element.text = str(value)

    etree.SubElement(
        element,
        "{http://www.broservices.nl/xsd/frdcommon/1.0}relatedMeasurementConfiguration",
        attrib={"{http://www.w3.org/1999/xlink}href": config_name},
    )