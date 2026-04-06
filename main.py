import json
import pathlib
import re

import xmlschema

schema: xmlschema.XMLSchema = xmlschema.XMLSchema(
    pathlib.Path("data/schema/aixm511/xsd/message/AIXM_BasicMessage.xsd")
)


for path in pathlib.Path("data/Baseline").iterdir():
    v: re.Match[str] | None = re.fullmatch(
        pattern=r"^CN_AIP-DS_([A-Za-z]+)_BASELINE_EFF\d{12}_AIRAC_V\d$",
        string=path.stem,
    )
    if v is None:
        continue

    output_path: pathlib.Path = pathlib.Path("output").joinpath(f"{v[1]}.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        data=json.dumps(
            obj=schema.to_dict(
                source=path,
            ),
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            default=str,
        ),
    )
