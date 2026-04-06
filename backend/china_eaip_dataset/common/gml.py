import datetime
import typing

import pydantic

from ..base import BaseModel
from .xlink import WithDollar


class WithAtGmlId(BaseModel):
    at_gml_id: typing.Annotated[
        str,
        pydantic.Field(alias="@gml:id"),
    ]


class _GmlBeginPosition(WithDollar[datetime.datetime]):
    at_frame: typing.Annotated[
        typing.Literal["#ISO-8601"],
        pydantic.Field(alias="@frame"),
    ]


class _GmlEndPosition(BaseModel):
    at_frame: typing.Annotated[
        typing.Literal["#ISO-8601"],
        pydantic.Field(alias="@frame"),
    ]
    at_indeterminate_position: typing.Annotated[
        typing.Literal["unknown"],
        pydantic.Field(alias="@indeterminatePosition"),
    ]


class _GmlTimePeriod(WithAtGmlId):
    at_frame: typing.Annotated[
        typing.Literal["#ISO-8601"],
        pydantic.Field(alias="@frame"),
    ]
    gml_begin_position: typing.Annotated[
        _GmlBeginPosition,
        pydantic.Field(alias="gml:beginPosition"),
    ]
    gml_end_position: typing.Annotated[
        _GmlEndPosition,
        pydantic.Field(alias="gml:endPosition"),
    ]


class WithGmlTimePeriod(BaseModel):
    gml_time_period: typing.Annotated[
        _GmlTimePeriod,
        pydantic.Field(alias="gml:TimePeriod"),
    ]
