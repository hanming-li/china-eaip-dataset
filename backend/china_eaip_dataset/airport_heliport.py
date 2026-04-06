import datetime
import decimal
import typing

import pydantic

from .base import BaseModel
from .common.gml import WithAtGmlId, WithGmlTimePeriod
from .common.xlink import WithAtOwns, WithAtXlinkType, WithDollar

_Latitude = typing.Annotated[float, pydantic.Field(ge=-90, le=90)]
_Longitude = typing.Annotated[float, pydantic.Field(ge=-180, le=180)]


class _Nil(BaseModel, validate_by_name=True):
    at_nil_reason: typing.Annotated[
        typing.Literal["unknown"],
        pydantic.Field(alias="@nilReason"),
    ]
    at_xmlns_xsi: typing.Annotated[
        typing.Literal["http://www.w3.org/2001/XMLSchema-instance"],
        pydantic.Field(alias="@xmlns:xsi"),
    ]
    at_xsi_nil: typing.Annotated[
        typing.Literal["true"],
        pydantic.Field(alias="@xsi:nil"),
    ]


class _Optional[Inner: typing.Any](BaseModel):
    value: Inner | None

    @pydantic.model_validator(mode="wrap")
    @classmethod
    def validate_nil(
        cls, data: typing.Any, handler: pydantic.ModelWrapValidatorHandler[typing.Self]
    ) -> typing.Self:
        try:
            _Nil.model_validate(obj=data, by_alias=True)
            return handler({"value": None})
        except pydantic.ValidationError:
            return handler({"value": data})

    @pydantic.model_serializer(mode="plain")
    def serialize_nil(self) -> Inner | _Nil:
        if self.value is None:
            return _Nil(
                at_nil_reason="unknown",
                at_xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance",
                at_xsi_nil="true",
            )
        return self.value


class _AixmElevatedPoint(WithAtGmlId):
    at_srs_name: typing.Annotated[
        typing.Literal["urn:ogc:def:crs:EPSG::4326"],
        pydantic.Field(alias="@srsName"),
    ]
    aixm_horizontal_accuracy: typing.Annotated[
        _Optional[None],
        pydantic.Field(alias="aixm:horizontalAccuracy"),
    ]
    gml_pos: typing.Annotated[
        tuple[_Latitude, _Longitude],
        pydantic.Field(alias="gml:pos"),
    ]


class _AixmArp(BaseModel):
    aixm_elevated_point: typing.Annotated[
        _AixmElevatedPoint,
        pydantic.Field(alias="aixm:ElevatedPoint"),
    ]


class _AixmNoteInner(WithDollar):
    at_lang: typing.Annotated[
        typing.Literal["eng"],
        pydantic.Field(alias="@lang"),
    ]


class _AixmLinguisticNote(WithAtGmlId):
    aixm_note: typing.Annotated[
        _AixmNoteInner,
        pydantic.Field(alias="aixm:note"),
    ]


class _AixmTranslatedNoteItem(BaseModel):
    aixm_linguistic_note: typing.Annotated[
        _AixmLinguisticNote,
        pydantic.Field(alias="aixm:LinguisticNote"),
    ]


class _AixmNoteOuter(WithAtGmlId):
    aixm_property_name: typing.Annotated[
        typing.Literal["ARP"],
        pydantic.Field(alias="aixm:propertyName"),
    ]
    aixm_purpose: typing.Annotated[
        typing.Literal["DESCRIPTION"],
        pydantic.Field(alias="aixm:purpose"),
    ]
    aixm_translated_note: typing.Annotated[
        tuple[_AixmTranslatedNoteItem],
        pydantic.Field(alias="aixm:translatedNote"),
    ]


class _AixmAnnotationItem(BaseModel):
    aixm_note: typing.Annotated[
        _AixmNoteOuter,
        pydantic.Field(alias="aixm:Note"),
    ]


class _AixmFlightCharacteristic(WithAtGmlId):
    aixm_military: typing.Annotated[
        typing.Literal["CIVIL"],
        pydantic.Field(alias="aixm:military"),
    ]
    aixm_purpose: typing.Annotated[
        _Optional[typing.Literal["SCHEDULED", "NON_SCHEDULED"]],
        pydantic.Field(alias="aixm:purpose"),
    ]
    aixm_rule: typing.Annotated[
        _Optional[typing.Literal["ALL"]],
        pydantic.Field(alias="aixm:rule"),
    ]
    aixm_type: typing.Annotated[
        _Optional[typing.Literal["OAT", "GAT"]],
        pydantic.Field(alias="aixm:type"),
    ]


class _AixmFlightItem(BaseModel):
    aixm_flight_characteristic: typing.Annotated[
        _AixmFlightCharacteristic,
        pydantic.Field(alias="aixm:FlightCharacteristic"),
    ]


class _AixmConditionCombination(WithAtGmlId):
    aixm_flight: typing.Annotated[
        tuple[_AixmFlightItem],
        pydantic.Field(alias="aixm:flight"),
    ]


class _AixmSelection(BaseModel):
    aixm_condition_combination: typing.Annotated[
        _AixmConditionCombination,
        pydantic.Field(alias="aixm:ConditionCombination"),
    ]


class _AixmAirportHeliportUsage(WithAtGmlId):
    aixm_selection: typing.Annotated[
        _AixmSelection,
        pydantic.Field(alias="aixm:selection"),
    ]


class _AixmUsageItem(BaseModel):
    aixm_airport_heliport_usage: typing.Annotated[
        _AixmAirportHeliportUsage,
        pydantic.Field(alias="aixm:AirportHeliportUsage"),
    ]


class _AixmAirportHeliportAvailability(WithAtGmlId):
    aixm_usage: typing.Annotated[
        list[_AixmUsageItem],
        pydantic.Field(alias="aixm:usage"),
    ]


class _AixmAvailabilityItem(BaseModel):
    aixm_airport_heliport_availability: typing.Annotated[
        _AixmAirportHeliportAvailability,
        pydantic.Field(alias="aixm:AirportHeliportAvailability"),
    ]


class _Unit[Unit: typing.Literal["M", "C"]](WithDollar[decimal.Decimal]):
    at_uom: typing.Annotated[
        Unit,
        pydantic.Field(alias="@uom"),
    ]


class _AixmCity(WithAtGmlId):
    aixm_name: typing.Annotated[
        str,
        pydantic.Field(alias="aixm:name"),
    ]


class _AixmServedCityItem(BaseModel):
    aixm_city: typing.Annotated[
        _AixmCity,
        pydantic.Field(alias="aixm:City"),
    ]


class _GmlValidTime(WithAtXlinkType, WithAtOwns, WithGmlTimePeriod):
    pass


class _AixmAirportHeliportTimeSlice(WithAtGmlId):
    aixm_arp: typing.Annotated[
        _AixmArp,
        pydantic.Field(alias="aixm:ARP"),
    ]
    aixm_annotation: typing.Annotated[
        tuple[_AixmAnnotationItem],
        pydantic.Field(alias="aixm:annotation"),
    ]
    aixm_availability: typing.Annotated[
        tuple[_AixmAvailabilityItem],
        pydantic.Field(alias="aixm:availability"),
    ]
    aixm_certification_date: typing.Annotated[
        datetime.date,
        pydantic.Field(alias="aixm:certificationDate"),
    ]
    aixm_certification_expiration_date: typing.Annotated[
        datetime.date,
        pydantic.Field(alias="aixm:certificationExpirationDate"),
    ]
    aixm_certified_icao: typing.Annotated[
        typing.Literal["YES"],
        pydantic.Field(alias="aixm:certifiedICAO"),
    ]
    aixm_control_type: typing.Annotated[
        typing.Literal["CIVIL"],
        pydantic.Field(alias="aixm:controlType"),
    ]
    aixm_correction_number: typing.Annotated[
        int,
        pydantic.Field(alias="aixm:correctionNumber"),
    ]
    aixm_date_magnetic_variation: typing.Annotated[
        _Optional[decimal.Decimal],
        pydantic.Field(alias="aixm:dateMagneticVariation"),
    ]
    aixm_designator: typing.Annotated[
        str,
        pydantic.Field(alias="aixm:designator"),
    ]
    aixm_designator_iata: typing.Annotated[
        str,
        pydantic.Field(alias="aixm:designatorIATA"),
    ]
    aixm_field_elevation: typing.Annotated[
        _Unit[typing.Literal["M"]],
        pydantic.Field(alias="aixm:fieldElevation"),
    ]
    aixm_field_elevation_accuracy: typing.Annotated[
        _Optional[None],
        pydantic.Field(alias="aixm:fieldElevationAccuracy"),
    ]
    aixm_interpretation: typing.Annotated[
        typing.Literal["BASELINE"],
        pydantic.Field(alias="aixm:interpretation"),
    ]
    aixm_location_indicator_icao: typing.Annotated[
        str,
        pydantic.Field(alias="aixm:locationIndicatorICAO"),
    ]
    aixm_magnetic_variation: typing.Annotated[
        decimal.Decimal,
        pydantic.Field(alias="aixm:magneticVariation"),
    ]
    aixm_magnetic_variation_accuracy: typing.Annotated[
        _Optional[None],
        pydantic.Field(alias="aixm:magneticVariationAccuracy"),
    ]
    aixm_magnetic_variation_change: typing.Annotated[
        _Optional[None],
        pydantic.Field(alias="aixm:magneticVariationChange"),
    ]
    aixm_name: typing.Annotated[
        str,
        pydantic.Field(alias="aixm:name"),
    ]
    aixm_reference_temperature: typing.Annotated[
        _Unit[typing.Literal["C"]],
        pydantic.Field(alias="aixm:referenceTemperature"),
    ]
    aixm_sequence_number: typing.Annotated[
        int,
        pydantic.Field(alias="aixm:sequenceNumber"),
    ]
    aixm_served_city: typing.Annotated[
        tuple[_AixmServedCityItem],
        pydantic.Field(alias="aixm:servedCity"),
    ]
    aixm_type: typing.Annotated[
        typing.Literal["AD"],
        pydantic.Field(alias="aixm:type"),
    ]
    gml_valid_time: typing.Annotated[
        _GmlValidTime,
        pydantic.Field(alias="gml:validTime"),
    ]


class _AixmTimeSliceItem(WithAtOwns):
    aixm_airport_heliport_time_slice: typing.Annotated[
        _AixmAirportHeliportTimeSlice,
        pydantic.Field(alias="aixm:AirportHeliportTimeSlice"),
    ]


class _GmlIdentifier(WithDollar):
    at_code_space: typing.Annotated[
        typing.Literal["urn:uuid:"],
        pydantic.Field(alias="@codeSpace"),
    ]


class _AixmAirportHeliport(WithAtGmlId):
    aixm_time_slice: typing.Annotated[
        tuple[_AixmTimeSliceItem],
        pydantic.Field(alias="aixm:timeSlice"),
    ]
    gml_identifier: typing.Annotated[
        _GmlIdentifier,
        pydantic.Field(alias="gml:identifier"),
    ]


class MessageHasMemberItem(WithAtXlinkType, WithAtOwns):
    aixm_airport_heliport: typing.Annotated[
        _AixmAirportHeliport,
        pydantic.Field(alias="aixm:AirportHeliport"),
    ]
