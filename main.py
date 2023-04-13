import aas_core3_rc02.types as aas_types
import math
import re
import aas_core3_rc02.jsonization as aas_jsonization
import json
import paho.mqtt.client as mqtt
import time

#region float to xs float
def float_to_xs_float(number: float) -> str:
    if math.isnan(number):
        return "NaN"
    elif math.isinf(number):
        if number > 0:
            return "INF"
        else:
            return "-INF"
    else:
        return str(number)

VALID_XS_STRING_RE = re.compile(
    r"^[\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD\U00010000-\U0010FFFF]*$"
)
#endregion

#region MQTT function
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "example/topic"

# Implement get_the_state_from_the_sensor() function
def get_the_state_from_the_sensor():
    return "Good"

temperature = aas_types.Property(
    value=float_to_xs_float(216.0),
    value_type=aas_types.DataTypeDefXsd.FLOAT,
    id_short="temperature",
    semantic_id=aas_types.Reference(
        type=aas_types.ReferenceTypes.MODEL_REFERENCE,
        keys=[
            aas_types.Key(
                type=aas_types.KeyTypes.CONCEPT_DESCRIPTION,
                value="urn:zhaw:conceptDescription:temperature"
            )
        ]
    )
)

state_value = get_the_state_from_the_sensor()
if VALID_XS_STRING_RE.match(state_value) is None:
    raise RuntimeError(f"Unexpected state value: {state_value}")

state = aas_types.Property(
    value=state_value,
    id_short="state",
    value_type=aas_types.DataTypeDefXsd.STRING
)
#endregion



# region real time data example submodel
submodel_chiller_real_time = aas_types.Submodel(
    id="urn:zhaw:ims:chiller:543fsfds99342:realTime",
    submodel_elements=[temperature, state]
)

#region Submodel identification

identification_attributes = [
    {"value": "Thermo-chiller", "id_short": "name", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "Circulating Fluid Temperature Controller Thermo chiller", "id_short": "full_name", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "yX488", "id_short": "serial_no", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "HRS050-AF-20", "id_short": "model", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "HRS", "id_short": "series", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "69", "id_short": "weight_kg", "value_type": aas_types.DataTypeDefXsd.INT},
    {"value": "976x377x592", "id_short": "size_mm", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "SMC (Japan)", "id_short": "manufacturer", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "HRX-OM-0020 HRX-OM-0021", "id_short": "manual", "value_type": aas_types.DataTypeDefXsd.STRING},
]

submodel_chiller_identification = aas_types.Submodel(
    id="urn:zhaw:ims:chiller:543fsfds99342:identification",
    submodel_elements=[
        aas_types.Property(
            value="Thermo-chiller",
            id_short="name",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="Circulating Fluid Temperature Controller Thermo chiller",
            id_short="full_name",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="yX488",
            id_short="serial_no",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="HRS050-AF-20",
            id_short="model",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="HRS",
            id_short="series",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="69",
            id_short="weight_kg",
            value_type=aas_types.DataTypeDefXsd.INT
        ),
        aas_types.Property(
            value="976x377x592",
            id_short="size_mm",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="SMC (Japan)",
            id_short="manufacturer",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="HRX-OM-0020 HRX-OM-0021",
            id_short="manual",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
    ]
)


#endregion

#region Submodel standard Technical data

standard_technical_data_attributes = [
    {"value": "2.5", "id_short": "capacity_aic_ka", "value_type": aas_types.DataTypeDefXsd.FLOAT},
    {"value": "30-70", "id_short": "humidity_range_percent", "value_type": aas_types.DataTypeDefXsd.STRING}, #AAS.TYPES.Range replace the property
    {"value": "3000", "id_short": "altitude_m", "value_type": aas_types.DataTypeDefXsd.INT},
    {"value": "R410A (HFC)", "id_short": "refrigerant", "value_type": aas_types.DataTypeDefXsd.STRING}, # could link to another URL or website (aas_types.DataTypeDefXsd.AnyURI)
    {"value": "0.65", "id_short": "refrigerant_charge_kg", "value_type": aas_types.DataTypeDefXsd.FLOAT},
    {"value": "PID control", "id_short": "control_method", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "65/68", "id_short": "noise_level_50Hz_60Hz_dB", "value_type": aas_types.DataTypeDefXsd.STRING}, #sperate the 50 and 60 Hz
]


submodel_chiller_standard_technical_data = aas_types.Submodel(
    id="urn:zhaw:ims:chiller:543fsfds99342:standard_technical_data",
    submodel_elements=[
        aas_types.Property(
            value="2.5",
            id_short="capacity_aic_ka",
            value_type=aas_types.DataTypeDefXsd.FLOAT
        ),
        aas_types.Property(
            value="30-70",
            id_short="humidity_range_percent",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),  # AAS.TYPES.Range should replace this property
        aas_types.Property(
            value="3000",
            id_short="altitude_m",
            value_type=aas_types.DataTypeDefXsd.INT
        ),
        aas_types.Property(
            value="R410A (HFC)",
            id_short="refrigerant",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),  # Could link to another URL or website (aas_types.DataTypeDefXsd.AnyURI)
        aas_types.Property(
            value="0.65",
            id_short="refrigerant_charge_kg",
            value_type=aas_types.DataTypeDefXsd.FLOAT
        ),
        aas_types.Property(
            value="PID control",
            id_short="control_method",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="65/68",
            id_short="noise_level_50Hz_60Hz_dB",
            value_type=aas_types.DataTypeDefXsd.STRING
        )
    ]
)

#endregion

#region Submodel standard circulating fluid system data

standard_circulating_fluid_system_data_attributes = [
    {"value": "Tap water", "id_short": "circulating_fluid", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "5-40", "id_short": "set_temperature_range_celsius", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "4700/5100", "id_short": "cooling_capacity_50Hz_60Hz_watt", "value_type": aas_types.DataTypeDefXsd.STRING}, #sep 50 /60 and string -> int
    {"value": "1100/1400", "id_short": "heating_capacity_50Hz_60Hz_watt", "value_type": aas_types.DataTypeDefXsd.STRING}, # the unit can be outside (remind Markco)
    {"value": "0.1", "id_short": "temperature_stability", "value_type": aas_types.DataTypeDefXsd.FLOAT},
    {"value": "23 (0.24 MPa)/28 (0.32 MPa)", "id_short": "pump_rated_flow_50Hz_60Hz_lmin", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "31/42", "id_short": "pump_max_flow_rate_50Hz_60Hz_lmin", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "50", "id_short": "pump_max_head_50Hz_60Hz_m", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "550", "id_short": "pump_output_W", "value_type": aas_types.DataTypeDefXsd.FLOAT},
    {"value": "5", "id_short": "tank_capacity_L", "value_type": aas_types.DataTypeDefXsd.FLOAT},
    {"value": "RC1/2", "id_short": "port_size", "value_type": aas_types.DataTypeDefXsd.FLOAT}
]



submodel_chiller_standard_circulating_fluid_system_data = aas_types.Submodel(
    id="urn:zhaw:ims:chiller:543fsfds99342:standard_circulating_fluid_system_data",
    submodel_elements=[
        aas_types.Property(
            value="Tap water",
            id_short="circulating_fluid",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="5-40",
            id_short="set_temperature_range_celsius",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="4700/5100",
            id_short="cooling_capacity_50Hz_60Hz_watt",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),  # Separate 50 / 60 Hz and convert string -> int
        aas_types.Property(
            value="1100/1400",
            id_short="heating_capacity_50Hz_60Hz_watt",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),  # The unit can be outside (remind Markco)
        aas_types.Property(
            value="0.1",
            id_short="temperature_stability",
            value_type=aas_types.DataTypeDefXsd.FLOAT
        ),
        aas_types.Property(
            value="23 (0.24 MPa)/28 (0.32 MPa)",
            id_short="pump_rated_flow_50Hz_60Hz_lmin",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="31/42",
            id_short="pump_max_flow_rate_50Hz_60Hz_lmin",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="50",
            id_short="pump_max_head_50Hz_60Hz_m",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="550",
            id_short="pump_output_W",
            value_type=aas_types.DataTypeDefXsd.FLOAT
        ),
        aas_types.Property(
            value="5",
            id_short="tank_capacity_L",
            value_type=aas_types.DataTypeDefXsd.FLOAT
        ),
        aas_types.Property(
            value="RC1/2",
            id_short="port_size",
            value_type=aas_types.DataTypeDefXsd.STRING
        )
    ]
)

#endregion

#region Submodel standard electrical system data

standard_electrical_system_data_attributes = [
    {"value": "200-230", "id_short": "power_supply_50Hz_60Hz_vac", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "20", "id_short": "circuit_protector_a", "value_type": aas_types.DataTypeDefXsd.FLOAT},
    {"value": "20", "id_short": "applicable_earth_leakage_breaker_capacity_a", "value_type": aas_types.DataTypeDefXsd.FLOAT},
    {"value": "8/11", "id_short": "rated_operating_current_a", "value_type": aas_types.DataTypeDefXsd.STRING},
    {"value": "1.7/2.2", "id_short": "rated_power_consumption_50Hz_60Hz_kva", "value_type": aas_types.DataTypeDefXsd.STRING}
]
submodel_chiller_standard_electrical_system_data = aas_types.Submodel(
    id="urn:zhaw:ims:chiller:543fsfds99342:standard_electrical_system_data",
    submodel_elements=[
        aas_types.Property(
            value="200-230",
            id_short="power_supply_50Hz_60Hz_vac",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="20",
            id_short="circuit_protector_a",
            value_type=aas_types.DataTypeDefXsd.FLOAT
        ),
        aas_types.Property(
            value="20",
            id_short="applicable_earth_leakage_breaker_capacity_a",
            value_type=aas_types.DataTypeDefXsd.FLOAT
        ),
        aas_types.Property(
            value="8/11",
            id_short="rated_operating_current_a",
            value_type=aas_types.DataTypeDefXsd.STRING
        ),
        aas_types.Property(
            value="1.7/2.2",
            id_short="rated_power_consumption_50Hz_60Hz_kva",
            value_type=aas_types.DataTypeDefXsd.STRING
        )
    ]
)


#endregion


#region example code of static submodel

# Add necessary properties to the submodel_elements list for submodel_chiller_static
prop1 = aas_types.Property(
    value="static_value1",
    id_short="prop1",
    value_type=aas_types.DataTypeDefXsd.STRING
)
prop2 = aas_types.Property(
    value="42",
    id_short="prop2",
    value_type=aas_types.DataTypeDefXsd.INT
)

submodel_chiller_static = aas_types.Submodel(
    id="urn:zhaw:ims:chiller:543fsfds99342:static",
    submodel_elements=[prop1, prop2]
)
#endregion

#region AAS information
asset_information = aas_types.AssetInformation(
    asset_kind=aas_types.AssetKind.TYPE # should be INSTANCE
)
#endregion


#region AAS model
chiller = aas_types.AssetAdministrationShell(
    id="urn:zhaw:ims:chiller:543fsfds99342",
    asset_information= asset_information ,
    submodels=[
        aas_types.Reference( #
            type=aas_types.ReferenceTypes.MODEL_REFERENCE,
            keys=[
                aas_types.Key(
                    type=aas_types.KeyTypes.SUBMODEL,
                    value="urn:zhaw:ims:chiller:543fsfds99342:realTime"
                )
            ]
        ),
        aas_types.Reference(
            type=aas_types.ReferenceTypes.MODEL_REFERENCE,
            keys=[
                aas_types.Key(
                    type=aas_types.KeyTypes.SUBMODEL,
                    value="urn:zhaw:ims:chiller:543fsfds99342:static"
                )
            ]
        ),
        aas_types.Reference(
            type=aas_types.ReferenceTypes.MODEL_REFERENCE,
            keys=[
                aas_types.Key(
                    type=aas_types.KeyTypes.SUBMODEL,
                    value="urn:zhaw:ims:chiller:543fsfds99342:identification"
                )
            ]
        ),
        aas_types.Reference(
            type=aas_types.ReferenceTypes.MODEL_REFERENCE,
            keys=[
                aas_types.Key(
                    type=aas_types.KeyTypes.SUBMODEL,
                    value="urn:zhaw:ims:chiller:543fsfds99342:standard_technical_data"
                )
            ]
        ),
        aas_types.Reference(
            type=aas_types.ReferenceTypes.MODEL_REFERENCE,
            keys=[
                aas_types.Key(
                    type=aas_types.KeyTypes.SUBMODEL,
                    value="urn:zhaw:ims:chiller:543fsfds99342:standard_circulating_fluid_system_data"
                )
            ]
        ),
        aas_types.Reference(
            type=aas_types.ReferenceTypes.MODEL_REFERENCE,
            keys=[
                aas_types.Key(
                    type=aas_types.KeyTypes.SUBMODEL,
                    value="urn:zhaw:ims:chiller:543fsfds99342:standard_electrical_system_data"
                )
            ]
        )

    ]
)
#endregion

#region AAS environment
# environment = want to send the aas AS a Json file.
environment = aas_types.Environment(
    submodels=[submodel_chiller_real_time,
               submodel_chiller_identification,
               submodel_chiller_standard_technical_data,
               submodel_chiller_standard_circulating_fluid_system_data,
               submodel_chiller_standard_electrical_system_data
               ],
    concept_descriptions=[
        aas_types.ConceptDescription(
            id="urn:zhaw:conceptDescription:temperature",
            embedded_data_specifications=[
                aas_types.EmbeddedDataSpecification(
                    data_specification=aas_types.Reference(
                        type=aas_types.ReferenceTypes.GLOBAL_REFERENCE,
                        keys=[
                            aas_types.Key(
                                type=aas_types.KeyTypes.GLOBAL_REFERENCE,
                                value="0112/2///61360_4#AAF927"
                            )
                        ]
                    ),
                    data_specification_content=aas_types.DataSpecificationIEC61360(
                        preferred_name=[
                            aas_types.LangString(
                                language="en",
                                text="tem"
                            )
                        ],
                        short_name=[
                            aas_types.LangString(
                                language="en",
                                text="p_water"
                            )
                        ],
                        definition=[
                            aas_types.LangString(
                                language="en",
                                text="pressure exerted on an object being completely embedded by water"
                            )
                        ],
                        unit="Pa"
                    )
                )
            ]
        )
    ]
)
#endregion

#region Serialize to a JSON-able mapping
jsonable = aas_jsonization.to_jsonable(environment)

# Print the mapping as text
print(json.dumps(jsonable, indent=3))
#endregion




while True:
    print(f"global data:")

    time.sleep(1)
