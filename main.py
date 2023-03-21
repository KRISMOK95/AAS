import aas_core3_rc02.types as aas_types
import math
import re

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

# Implement get_the_data_from_the_sensor() function
def get_the_data_from_the_sensor():
    return 10.0

# Implement get_the_state_from_the_sensor() function
def get_the_state_from_the_sensor():
    return "Good"

temperature = aas_types.Property(
    value=float_to_xs_float(get_the_data_from_the_sensor()),
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

# the id: urn:"urn:zhaw:ims:chiller:S/N number :static" (like a link)
# why FASTAPI required ?
