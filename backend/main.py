import decimal
import functools
import json
import pathlib
import re
import typing

import china_eaip_dataset
import fastapi
import pydantic
import uvicorn
import xmlschema

Longitude = typing.Annotated[
    float,
    pydantic.Field(
        allow_inf_nan=False,
        description="Positive for E; Negative for W.",
        ge=-180,
        le=180,
        title="Longitude / Easting",
    ),
]
Latitude = typing.Annotated[
    float,
    pydantic.Field(
        allow_inf_nan=False,
        description="Positive for N; Negative for S.",
        ge=-90,
        le=90,
        title="Latitude / Northing",
    ),
]
Altitude = typing.Annotated[
    float,
    pydantic.Field(
        allow_inf_nan=False,
        description="In meter. 1 ft = 0.3048 m.",
        title="Altitude / Elevation",
    ),
]
Position3D = typing.Annotated[
    tuple[Longitude, Latitude, Altitude],
    pydantic.Field(
        description="(longitude, latitude, altitude)",
        examples=[(116.391220088889, 39.9073541194444, 110)],
        title="GeoJSON Position w/ Altitude",
    ),
]


class _Point(pydantic.BaseModel, title="GeoJSON Point"):
    type: typing.Literal["Point"] = "Point"
    coordinates: Position3D


class _Feature[Geometry: _Point, Properties: typing.Any](
    pydantic.BaseModel, title="GeoJSON Feature"
):
    type: typing.Literal["Feature"] = "Feature"
    geometry: Geometry
    properties: Properties
    id: str


class _AirportHeliportProperties(pydantic.BaseModel):
    city: str
    name: str
    icao: str
    iata: str
    reference_temperature_in_celcius: decimal.Decimal
    magnetic_variation: decimal.Decimal


web_app = fastapi.FastAPI(debug=True)
data_path = pathlib.Path("../data")
schema: xmlschema.XMLSchema = xmlschema.XMLSchema(
    data_path.joinpath("schema/aixm511/xsd/message/AIXM_BasicMessage.xsd")
)


class File:
    xml_path: pathlib.Path

    def __init__(self, path: pathlib.Path) -> None:
        self.xml_path = path

    @functools.cached_property
    def key(self) -> typing.Literal["AirportHeliport"]:
        m: re.Match[str] | None = re.fullmatch(
            pattern=r"CN_AIP-DS_([A-Za-z]+?)_BASELINE_EFF(\d{12})_AIRAC_V(\d)",
            string=self.xml_path.stem,
        )
        if m is None or m[1] != "AirportHeliport":
            raise ValueError("文件名不对")
        return "AirportHeliport"

    @functools.cached_property
    def output_path(self) -> pathlib.Path:
        return pathlib.Path("output").joinpath(f"{self.key}.json")

    @functools.cached_property
    def raw_content(self) -> typing.Any:
        return schema.to_dict(source=self.xml_path)

    @functools.cached_property
    def input_text(self) -> str:
        return json.dumps(obj=self.raw_content, sort_keys=True, default=str)

    @functools.cached_property
    def model(self) -> china_eaip_dataset.Root:
        return china_eaip_dataset.Root.model_validate(obj=self.raw_content)

    @functools.cached_property
    def output_text(self) -> str:
        return json.dumps(
            obj=self.model.model_dump(
                mode="json", by_alias=True, exclude_defaults=True
            ),
            sort_keys=True,
        )


@web_app.get(path="/api/airports-heliports")
def list_all_airports_heliports() -> list[_Feature[_Point, _AirportHeliportProperties]]:
    for path in data_path.joinpath("Baseline").iterdir():
        if "AirportHeliport" not in path.stem:
            continue
        file: File = File(path=path)
        file.output_path.parent.mkdir(parents=True, exist_ok=True)
        assert file.input_text == file.output_text
        return sorted(
            [
                _Feature[_Point, _AirportHeliportProperties](
                    geometry=_Point(
                        coordinates=(
                            round(
                                x.aixm_airport_heliport.aixm_time_slice[
                                    0
                                ].aixm_airport_heliport_time_slice.aixm_arp.aixm_elevated_point.gml_pos[
                                    1
                                ],
                                6,
                            ),
                            round(
                                x.aixm_airport_heliport.aixm_time_slice[
                                    0
                                ].aixm_airport_heliport_time_slice.aixm_arp.aixm_elevated_point.gml_pos[
                                    0
                                ],
                                6,
                            ),
                            round(
                                float(
                                    x.aixm_airport_heliport.aixm_time_slice[
                                        0
                                    ].aixm_airport_heliport_time_slice.aixm_field_elevation.dollar
                                ),
                                1,
                            ),
                        )
                    ),
                    properties=_AirportHeliportProperties(
                        city=x.aixm_airport_heliport.aixm_time_slice[0]
                        .aixm_airport_heliport_time_slice.aixm_served_city[0]
                        .aixm_city.aixm_name.capitalize(),
                        name=x.aixm_airport_heliport.aixm_time_slice[
                            0
                        ].aixm_airport_heliport_time_slice.aixm_name.capitalize(),
                        icao=x.aixm_airport_heliport.aixm_time_slice[
                            0
                        ].aixm_airport_heliport_time_slice.aixm_location_indicator_icao.upper(),
                        iata=x.aixm_airport_heliport.aixm_time_slice[
                            0
                        ].aixm_airport_heliport_time_slice.aixm_designator_iata.upper(),
                        reference_temperature_in_celcius=x.aixm_airport_heliport.aixm_time_slice[
                            0
                        ].aixm_airport_heliport_time_slice.aixm_reference_temperature.dollar,
                        magnetic_variation=x.aixm_airport_heliport.aixm_time_slice[
                            0
                        ].aixm_airport_heliport_time_slice.aixm_magnetic_variation,
                    ),
                    id=x.aixm_airport_heliport.at_gml_id,
                )
                for x in file.model.message_has_member
            ],
            key=lambda x: (x.properties.icao),
        )
    raise FileNotFoundError


if __name__ == "__main__":
    uvicorn.run(app="main:web_app", reload=True)
