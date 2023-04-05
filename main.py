import aas_core3_rc02.types as aas_types
import math
import re
import aas_core3_rc02.jsonization as aas_jsonization
import json
import paho.mqtt.client as mqtt
import time
import threading
import logging
import functools




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
MQTT_TOPIC = "academics/IoT"

received_data_global = None
data_lock = threading.Lock()
def on_message(current_data_property, client, userdata, message):
    global temperature
    global received_data_global
    payload_str = message.payload.decode('utf-8')
    received_data = json.loads(payload_str)
    print(f"Received data from the Node-red script: {received_data}")

    with data_lock:
        received_data_global = received_data

    temp_value = received_data['data'][0]
    current_data_property.value = json.dumps(received_data)

    # Update the temperature and state properties with the new data
    temperature.value = float_to_xs_float(temp_value)
    print(f"real-time tem value: {temperature.value}")
    print(f"temp_value: {temp_value}")
    state.value = get_the_state_from_the_sensor()

def get_received_data():
    with data_lock:
        return received_data_global

# Set up the MQTT client and connect to the broker
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883)

# Set up the callback function to be called when a message is received
client.on_message = functools.partial(on_message, current_data_property)

# Subscribe to the MQTT topic
client.subscribe(MQTT_TOPIC)

# Start the MQTT client loop to listen for incoming messages
client.loop_start()

# Implement get_the_state_from_the_sensor() function
def get_the_state_from_the_sensor():
    return "Good"

temperature = aas_types.Property(
    value=float_to_xs_float(0.0),
    value_type=aas_types.DataTypeDefXsd.FLOAT,
    id_short="temperature"
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

#region Submodel real time row data

current_data_property = aas_types.Property(
    value="{}",
    id_short="realTimeRowData",
    value_type=aas_types.DataTypeDefXsd.STRING
)

submodel_chiller_real_time = aas_types.Submodel(
    id="urn:zhaw:ims:chiller:543fsfds99342:realTime",
    submodel_elements=[temperature, state,current_data_property ]
)

#endregion

#region real time data log

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zhaw_aas_server")

# Define the lock to protect the shared data (submodel properties)
submodel_realtime_data_lock = threading.Lock()

# Function to simulate retrieving real-time values
def get_realtime_values():
    received_data = get_received_data()
    if received_data is not None:
        return received_data
    else:
        return{}

# Define the update thread function
def update_thread() -> None:
    # List of submodels with real-time values
    realtime_submodels = [
        submodel_chiller_row_realtime_data,
        submodel_chiller_operation_realtime_data,
        submodel_chiller_status_flag_realtime_data,
        submodel_chiller_alarm_flag_realtime_data,
        submodel_chiller_fault_realtime_data
    ]

    while True:
        with submodel_realtime_data_lock:
            values = get_realtime_values()

            logger.info("Updating real-time values: %s", values)

            if values:  # Only update if the values dictionary is not empty
                for submodel in realtime_submodels:
                    for prop in submodel.submodel_elements:
                        if prop.id_short in values:
                            prop.value = values[prop.id_short]

        time.sleep(5)  # Update every 5 seconds


# Start the update thread
update_thread = threading.Thread(target=update_thread)
update_thread.start()

#endregion

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
               ]
)
#endregion

#region Serialize to a JSON-able mapping
jsonable = aas_jsonization.to_jsonable(environment)

# Print the mapping as text
print(json.dumps(jsonable, indent=3))
#endregion



try:
    while True:
        current_data = get_received_data()
        if current_data is not None:
            print(f"global data: {current_data}")

        time.sleep(1)
except KeyboardInterrupt:
    print("Terminating the script")
    client.loop_stop()  # Stop the MQTT client loop
