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



temperature = aas_types.Property(
    value="10", #value=float_to_xs_float(get_the_data_from_the_sensor())
    value_type=aas_types.DataTypeDefXsd.FLOAT,
    id_short="temperature"
)

state_value = get_the_state_from_the_sensor() # state_value = get_the_state_from_the_sensor()
if VALID_XS_STRING_RE.match(state_value) is None:
    raise RuntimeError(f"Unexpected state value: {state_value}")

state = aas_types.Property(
    value="Good", # state0 value
    id_short="state",
    value_type=aas_types.DataTypeDefXsd.STRING
)

submodel_chiller_real_time = aas_types.Submodel(
    id="urn:zhaw:ims:chiller:543fsfds99342:realTime",
    submodel_elements=[temperature, state]
)

submodel_chiller_static = aas_types.Submodel(
    id="urn:zhaw:ims:chiller:543fsfds99342:static",
    submodel_elements=[...]
)

chiller = aas_types.AssetAdministrationShell(
    id="urn:zhaw:ims:chiller:543fsfds99342",
    submodels=[
        aas_types.Reference(   # reference(type: reference types , keys:list[key], referred semantic id)
            modelType=aas_types.ModelReference,
            keys=[
                aas_types.Key(
                    key_type=aas_types.KeyTypes.Submodel,
                    value="urn:zhaw:ims:chiller:543fsfds99342:realTime"
                )
            ]
        ),
        aas_types.Reference(
            modelType=aas_types.ModelReference,
            keys=[
                aas_types.Key(
                    key_type=aas_types.KeyTypes.Submodel,
                    value="urn:zhaw:ims:chiller:543fsfds99342:static"
                )
            ]
        )
    ]
)
