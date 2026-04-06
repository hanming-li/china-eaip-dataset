import typing

import pydantic

from ..base import BaseModel


class WithAtOwns(BaseModel):
    at_owns: typing.Annotated[
        typing.Literal[False],
        pydantic.Field(alias="@owns"),
    ]


class WithAtXlinkType(BaseModel):
    at_xlink_type: typing.Annotated[
        typing.Literal["simple"],
        pydantic.Field(alias="@xlink:type"),
    ]


class WithDollar[Inner: typing.Any = str](BaseModel):
    dollar: typing.Annotated[
        Inner,
        pydantic.Field(alias="$"),
    ]
