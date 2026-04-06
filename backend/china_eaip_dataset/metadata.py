import datetime
import typing

import pydantic

from .base import BaseModel
from .common.gml import WithGmlTimePeriod
from .common.xlink import WithAtOwns, WithAtXlinkType, WithDollar


class _WithGcoCharacterString[Inner: str = str](BaseModel):
    gco_character_string: typing.Annotated[
        Inner,
        pydantic.Field(alias="gco:CharacterString"),
    ]


class _WithGcoDateTime(BaseModel):
    gco_date_time: typing.Annotated[
        datetime.datetime,
        pydantic.Field(alias="gco:DateTime"),
    ]


class _GmxCodeLists[CodeList: str, CodeListValue: str](WithDollar[CodeListValue]):
    at_code_list: typing.Annotated[
        CodeList,
        pydantic.Field(alias="@codeList"),
    ]
    at_code_list_value: typing.Annotated[
        CodeListValue,
        pydantic.Field(alias="@codeListValue"),
    ]


class _GmdCiAddress(BaseModel):
    gmd_administrative_area: typing.Annotated[
        _WithGcoCharacterString[typing.Literal["Beijing"]],
        pydantic.Field(alias="gmd:administrativeArea"),
    ]
    gmd_city: typing.Annotated[
        _WithGcoCharacterString[typing.Literal["Beijing"]],
        pydantic.Field(alias="gmd:city"),
    ]
    gmd_country: typing.Annotated[
        _WithGcoCharacterString[typing.Literal["China"]],
        pydantic.Field(alias="gmd:country"),
    ]
    gmd_delivery_point: typing.Annotated[
        tuple[
            _WithGcoCharacterString[
                typing.Literal[
                    "No.9 Xiedao West Road, Chaoyang District Beijing 100018, People's Republic of China"
                ]
            ]
        ],
        pydantic.Field(alias="gmd:deliveryPoint"),
    ]
    gmd_electronic_mail_address: typing.Annotated[
        tuple[_WithGcoCharacterString[typing.Literal["aipchina@atmb.net.cn"]]],
        pydantic.Field(alias="gmd:electronicMailAddress"),
    ]
    gmd_postal_code: typing.Annotated[
        _WithGcoCharacterString[typing.Literal["100018"]],
        pydantic.Field(alias="gmd:postalCode"),
    ]


class _GmdAddress(WithAtXlinkType):
    gmd_ci_address: typing.Annotated[
        _GmdCiAddress,
        pydantic.Field(alias="gmd:CI_Address"),
    ]


class _GmdCiTelephone(BaseModel):
    gmd_voice: typing.Annotated[
        tuple[_WithGcoCharacterString[typing.Literal["86-10-57803699"]]],
        pydantic.Field(alias="gmd:voice"),
    ]


class _GmdPhone(WithAtXlinkType):
    gmd_ci_telephone: typing.Annotated[
        _GmdCiTelephone,
        pydantic.Field(alias="gmd:CI_Telephone"),
    ]


class _GmdCiContact(BaseModel):
    gmd_address: typing.Annotated[
        _GmdAddress,
        pydantic.Field(alias="gmd:address"),
    ]
    gmd_phone: typing.Annotated[
        _GmdPhone,
        pydantic.Field(alias="gmd:phone"),
    ]


class _GmdContactInfo(WithAtXlinkType):
    gmd_ci_contact: typing.Annotated[
        _GmdCiContact,
        pydantic.Field(alias="gmd:CI_Contact"),
    ]


class _GmdRole(BaseModel):
    gmd_ci_role_code: typing.Annotated[
        _GmxCodeLists[
            typing.Literal[
                "http://www.aixm.aero/schema/5.1/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#CI_RoleCode"
            ],
            typing.Literal["publisher"],
        ],
        pydantic.Field(alias="gmd:CI_RoleCode"),
    ]


class _GmdCiResponsibleParty(BaseModel):
    gmd_contact_info: typing.Annotated[
        _GmdContactInfo,
        pydantic.Field(alias="gmd:contactInfo"),
    ]
    gmd_organisation_name: typing.Annotated[
        _WithGcoCharacterString[
            typing.Literal[
                "Aeronautical Information Service Center of Air Traffic Management Bureau, Civil Aviation Administration of China"
            ]
        ],
        pydantic.Field(alias="gmd:organisationName"),
    ]
    gmd_role: typing.Annotated[
        _GmdRole,
        pydantic.Field(alias="gmd:role"),
    ]


class _GmdContactItem(WithAtXlinkType):
    gmd_ci_responsible_party: typing.Annotated[
        _GmdCiResponsibleParty,
        pydantic.Field(alias="gmd:CI_ResponsibleParty"),
    ]


class _GmdDateType(BaseModel):
    gmd_ci_date_type_code: typing.Annotated[
        _GmxCodeLists[
            typing.Literal[
                "http://www.aixm.aero/schema/5.1/ISO_19139_Schemas/resources/Codelist/gmxCodeLists.xml#CI_DateTypeCode"
            ],
            typing.Literal["revision"],
        ],
        pydantic.Field(alias="gmd:CI_DateTypeCode"),
    ]


class _GmdCiDate(BaseModel):
    gmd_date: typing.Annotated[
        _WithGcoDateTime,
        pydantic.Field(alias="gmd:date"),
    ]
    gmd_date_type: typing.Annotated[
        _GmdDateType,
        pydantic.Field(alias="gmd:dateType"),
    ]


class _GmdDate(WithAtXlinkType):
    gmd_ci_date: typing.Annotated[
        _GmdCiDate,
        pydantic.Field(alias="gmd:CI_Date"),
    ]


class _GmdCiCitation(BaseModel):
    gmd_date: typing.Annotated[
        tuple[_GmdDate],
        pydantic.Field(alias="gmd:date"),
    ]
    gmd_title: typing.Annotated[
        _WithGcoCharacterString[typing.Literal["Date and time when provided"]],
        pydantic.Field(alias="gmd:title"),
    ]


class _GmdCitation(WithAtXlinkType):
    gmd_ci_citation: typing.Annotated[
        _GmdCiCitation,
        pydantic.Field(alias="gmd:CI_Citation"),
    ]


class _GmdExtent(WithAtXlinkType, WithGmlTimePeriod):
    pass


class _GmdExTemporalExtent(BaseModel):
    gmd_extent: typing.Annotated[
        _GmdExtent,
        pydantic.Field(alias="gmd:extent"),
    ]


class _GmdTemporalElementItem(WithAtXlinkType):
    gmd_ex_temporal_extent: typing.Annotated[
        _GmdExTemporalExtent,
        pydantic.Field(alias="gmd:EX_TemporalExtent"),
    ]


class _GmdExExtentA(BaseModel):
    gmd_temporal_element: typing.Annotated[
        tuple[_GmdTemporalElementItem],
        pydantic.Field(alias="gmd:temporalElement"),
    ]


class _GmdExExtentB(BaseModel):
    gmd_description: typing.Annotated[
        _WithGcoCharacterString[typing.Literal["AIRAC"]],
        pydantic.Field(alias="gmd:description"),
    ]


class _GmdExtentItem(WithAtXlinkType):
    gmd_ex_extent: typing.Annotated[
        _GmdExExtentA | _GmdExExtentB,
        pydantic.Field(alias="gmd:EX_Extent"),
    ]


class _GmdMdConstraints(BaseModel):
    gmd_use_limitation: typing.Annotated[
        tuple[
            _WithGcoCharacterString[
                typing.Literal[
                    "For evaluation and testing use only; not for operational purposes."
                ]
            ]
        ],
        pydantic.Field(alias="gmd:useLimitation"),
    ]


class _GmdResourceConstraintsItem(WithAtXlinkType):
    gmd_md_constraints: typing.Annotated[
        _GmdMdConstraints,
        pydantic.Field(alias="gmd:MD_Constraints"),
    ]


class _GmdSpatialRepresentationTypeItem(BaseModel):
    gmd_md_spatial_representation_type_code: typing.Annotated[
        _GmxCodeLists[
            typing.Literal[
                "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/ML_gmxCodelists.xml#MD_SpatialRepresentationTypeCode"
            ],
            typing.Literal["vector"],
        ],
        pydantic.Field(alias="gmd:MD_SpatialRepresentationTypeCode"),
    ]


class _GmdMdDataIdentification(BaseModel):
    gmd_abstract: typing.Annotated[
        _WithGcoCharacterString[
            typing.Literal[
                "The aeronautical data for People's Republic of China are collected and published according to ICAO Annex 15, 16th Edition requirements. Refer to the DPS document for detail information."
            ]
        ],
        pydantic.Field(alias="gmd:abstract"),
    ]
    gmd_citation: typing.Annotated[
        _GmdCitation,
        pydantic.Field(alias="gmd:citation"),
    ]
    gmd_extent: typing.Annotated[
        tuple[_GmdExtentItem, _GmdExtentItem],
        pydantic.Field(alias="gmd:extent"),
    ]
    gmd_language: typing.Annotated[
        tuple[_WithGcoCharacterString[typing.Literal["eng"]]],
        pydantic.Field(alias="gmd:language"),
    ]
    gmd_point_of_contact: typing.Annotated[
        tuple[_GmdContactItem],
        pydantic.Field(alias="gmd:pointOfContact"),
    ]
    gmd_resource_constraints: typing.Annotated[
        tuple[_GmdResourceConstraintsItem],
        pydantic.Field(alias="gmd:resourceConstraints"),
    ]
    gmd_spatial_representation_type: typing.Annotated[
        tuple[_GmdSpatialRepresentationTypeItem],
        pydantic.Field(alias="gmd:spatialRepresentationType"),
    ]


class _GmdIdentificationInfoItem(WithAtXlinkType):
    gmd_md_data_identification: typing.Annotated[
        _GmdMdDataIdentification,
        pydantic.Field(alias="gmd:MD_DataIdentification"),
    ]


class _GmdMdMetadata(BaseModel):
    at_id: typing.Annotated[
        str,
        pydantic.Field(alias="@id"),
    ]
    gmd_contact: typing.Annotated[
        tuple[_GmdContactItem],
        pydantic.Field(alias="gmd:contact"),
    ]
    gmd_date_stamp: typing.Annotated[
        _WithGcoDateTime,
        pydantic.Field(alias="gmd:dateStamp"),
    ]
    gmd_identification_info: typing.Annotated[
        tuple[_GmdIdentificationInfoItem],
        pydantic.Field(alias="gmd:identificationInfo"),
    ]


class AixmMessageMetadata(WithAtOwns):
    gmd_md_metadata: typing.Annotated[
        _GmdMdMetadata,
        pydantic.Field(alias="gmd:MD_Metadata"),
    ]
