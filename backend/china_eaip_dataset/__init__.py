import typing

import pydantic

from .airport_heliport import MessageHasMemberItem as AirportHeliport
from .common.gml import WithAtGmlId
from .metadata import AixmMessageMetadata


class Root(WithAtGmlId):
    at_xmlns_aixm: typing.Annotated[
        typing.Literal["http://www.aixm.aero/schema/5.1.1"],
        pydantic.Field(alias="@xmlns:aixm"),
    ]
    at_xmlns_gco: typing.Annotated[
        typing.Literal["http://www.isotc211.org/2005/gco"],
        pydantic.Field(alias="@xmlns:gco"),
    ]
    at_xmlns_gmd: typing.Annotated[
        typing.Literal["http://www.isotc211.org/2005/gmd"],
        pydantic.Field(alias="@xmlns:gmd"),
    ]
    at_xmlns_gml: typing.Annotated[
        typing.Literal["http://www.opengis.net/gml/3.2"],
        pydantic.Field(alias="@xmlns:gml"),
    ]
    at_xmlns_gsr: typing.Annotated[
        typing.Literal["http://www.isotc211.org/2005/gsr"],
        pydantic.Field(alias="@xmlns:gsr"),
    ]
    at_xmlns_gss: typing.Annotated[
        typing.Literal["http://www.isotc211.org/2005/gss"],
        pydantic.Field(alias="@xmlns:gss"),
    ]
    at_xmlns_gts: typing.Annotated[
        typing.Literal["http://www.isotc211.org/2005/gts"],
        pydantic.Field(alias="@xmlns:gts"),
    ]
    at_xmlns_message: typing.Annotated[
        typing.Literal["http://www.aixm.aero/schema/5.1.1/message"],
        pydantic.Field(alias="@xmlns:message"),
    ]
    at_xmlns_xlink: typing.Annotated[
        typing.Literal["http://www.w3.org/1999/xlink"],
        pydantic.Field(alias="@xmlns:xlink"),
    ]
    aixm_message_metadata: typing.Annotated[
        AixmMessageMetadata,
        pydantic.Field(alias="aixm:messageMetadata"),
    ]
    message_has_member: typing.Annotated[
        list[AirportHeliport],
        pydantic.Field(alias="message:hasMember"),
    ]
