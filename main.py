import aas_core3_rc02.types as aas_types
import math
import re
import aas_core3_rc02.jsonization as aas_jsonization
import json
import paho.mqtt.client as mqtt
import time

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

# MQTT function
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "AAS/data"


def on_message(client, userdata, message):
    payload_str = message.payload.decode('utf-8')
    received_data = json.loads(payload_str)
    print(f"Received data from the Node-red script: {received_data}")

    # Update the temperature and state properties with the new data
    temperature.value = float_to_xs_float(received_data[0])
    state.value = get_the_state_from_the_sensor()


# Set up the MQTT client and connect to the broker
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883)

# Set up the callback function to be called when a message is received
client.on_message = on_message

# Subscribe to the MQTT topic
client.subscribe(MQTT_TOPIC)

# Start the MQTT client loop to listen for incoming messages
client.loop_start()
# Implement get_the_data_from_the_sensor() function

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

submodel_chiller_real_time = aas_types.Submodel(
    id="urn:zhaw:ims:chiller:543fsfds99342:realTime",
    submodel_elements=[temperature, state]
)

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

asset_information = aas_types.AssetInformation(
    asset_kind=aas_types.AssetKind.TYPE # should be INSTANCE
)




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
        )
    ]
)

# Prepare the environment
# environment = want to send the aas AS a Json file.
environment = aas_types.Environment(
    submodels=[submodel_chiller_real_time]
)

# Serialize to a JSON-able mapping
jsonable = aas_jsonization.to_jsonable(environment)

# Print the mapping as text
print(json.dumps(jsonable, indent=2))


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Terminating the script")
    client.loop_stop()  # Stop the MQTT client loop
