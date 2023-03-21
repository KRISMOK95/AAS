import json

import aas_core3_rc02.types as aas_types
import aas_core3_rc02.jsonization as aas_jsonization

# Prepare the environment
environment = aas_types.Environment(
    submodels=[
        aas_types.Submodel(
            id="some-unique-global-identifier",
            submodel_elements=[
                aas_types.Property(
                    id_short = "some_property",
                    value_type=aas_types.DataTypeDefXsd.INT,
                    value="1984"
                )
            ]
        )
    ]
)

# Serialize to a JSON-able mapping
jsonable = aas_jsonization.to_jsonable(environment)

# Print the mapping as text
print(json.dumps(jsonable, indent=2))