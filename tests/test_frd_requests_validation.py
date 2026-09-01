from bro_exchange.broxml.frd import requests as frd_requests_module

METADATA = {"request_reference": "frd-ref-001", "quality_regime": "IMBRO"}


def test_frd_start_registration_generates_expected_root_and_namespace():
    tool = frd_requests_module.FRDStartRegistrationTool(
        metadata=METADATA,
        srcdocdata={
            "object_id_accountable_party": "obj-001",
            "gmn_bro_id": None,
            "gmw_bro_id": "GMW000000123456",
            "gmw_tube_number": "1",
        },
        request_type="registration",
    )
    tree = tool.generate_xml_file()
    root = tree.getroot()

    assert root.tag == "registrationRequest"
    assert root.find("sourceDocument/{http://www.broservices.nl/xsd/isfrd/1.0}FRD_StartRegistration") is not None


def test_frd_closure_tool_generates_expected_root_for_delete():
    tool = frd_requests_module.FRDClosureTool(
        metadata=METADATA,
        srcdocdata={},
        request_type="delete",
    )
    tree = tool.generate_xml_file()
    root = tree.getroot()

    assert root.tag == "deleteRequest"
    assert root.find("sourceDocument/{http://www.broservices.nl/xsd/isfrd/1.0}FRD_Closure") is not None


def test_gem_configuration_tool_generates_expected_root():
    tool = frd_requests_module.GEMConfigurationTool(
        metadata=METADATA,
        srcdocdata={
            "measurement_configurations": [
                {
                    "name": "mc1",
                    "measurement_pair": {
                        "elektrode1": {"cable_number": 1, "electrode_number": 1},
                        "elektrode2": {"cable_number": 1, "electrode_number": 2},
                    },
                    "flowcurrent_pair": {
                        "elektrode1": {"cable_number": 2, "electrode_number": 1},
                        "elektrode2": {"cable_number": 2, "electrode_number": 2},
                    },
                }
            ]
        },
        request_type="registration",
    )
    tree = tool.generate_xml_file()
    root = tree.getroot()

    assert root.tag == "registrationRequest"
    assert root.find("sourceDocument/FRD_GEM_MeasurementConfiguration") is not None


def test_gem_measurement_tool_generates_expected_root():
    tool = frd_requests_module.GEMMeasurementTool(
        metadata=METADATA,
        srcdocdata={
            "measurement_date": "2024-01-01",
            "measuring_responsible_party": "12345678",
            "measuring_procedure": "onbekend",
            "evaluation_procedure": "onbekend",
            "measurements": [("mc1", 1.23)],
            "calculated_method_responsible_party": "12345678",
            "calculated_method_procedure": "onbekend",
            "measurement_count": 1,
            "calculated_values": "1.23",
        },
        request_type="registration",
    )
    tree = tool.generate_xml_file()
    root = tree.getroot()

    assert root.tag == "registrationRequest"
    assert root.find("sourceDocument/FRD_GEM_Measurement") is not None


def test_emm_configuration_tool_generates_expected_root():
    tool = frd_requests_module.EMMConfigurationTool(
        metadata=METADATA,
        srcdocdata={
            "instrument_configuration_id": "ic1",
            "relative_position_transmitter_coil": "100",
            "relative_position_primary_receiver_coil": "50",
            "secondary_receiver_coil_available": "nee",
            "coil_frequency_known": "nee",
            "instrument_length": "150",
        },
        request_type="registration",
    )
    tree = tool.generate_xml_file()
    root = tree.getroot()

    assert root.tag == "registrationRequest"
    assert root.find("sourceDocument/FRD_EMM_InstrumentConfiguration") is not None


def test_emm_measurement_tool_generates_expected_root():
    tool = frd_requests_module.EMMMeasurementTool(
        metadata=METADATA,
        srcdocdata={
            "measurement_date": "2024-01-01",
            "measuring_responsible_party": "12345678",
            "measuring_procedure": "onbekend",
            "evaluation_procedure": "onbekend",
            "element_count": 1,
            "measurement_data": "1.23",
            "related_instrument_config": "ic1",
            "calculated_measurement_operator": "12345678",
            "calculated_determination_procedure": "onbekend",
            "formation_measurement_data_count": 1,
            "formation_measurement_data": "1.23",
        },
        request_type="registration",
    )
    tree = tool.generate_xml_file()
    root = tree.getroot()

    assert root.tag == "registrationRequest"
    assert root.find("sourceDocument/FRD_EMM_Measurement") is not None
