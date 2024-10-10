import datetime as dt
from enum import Enum
from typing import Annotated, Any, Optional

import pydantic
from pydantic import AfterValidator, BaseModel, Field, HttpUrl, RootModel

INPUT_DATE_FORMAT = "%Y-%m-%dT%H:%M"


def check_date_format(value: str) -> dt.datetime:
    """Makes sure the datetime format matches what the MOTD and CEDA status page expect"""
    return dt.datetime.strptime(value, INPUT_DATE_FORMAT)


class Status(Enum):
    """A set of pre-defined statuses for an incident"""

    DOWN = "down"
    RESOLVED = "resolved"
    DEGRADED = "degraded"
    AT_RISK = "at risk"


class Update(BaseModel):
    """An update contains further details and an optional URL for more info"""

    date: Annotated[str, AfterValidator(check_date_format)]
    details: str
    url: Optional[HttpUrl] = None

    @pydantic.field_serializer("date")
    def serialize_date(
        self, date: dt.datetime, _info: pydantic.FieldSerializationInfo
    ) -> str:
        return str(date.strftime(INPUT_DATE_FORMAT))


class Incident(BaseModel):
    """An incident contains details and a list of updates associated with it"""

    status: Status
    affectedServices: str
    summary: str
    date: Annotated[str, AfterValidator(check_date_format)]
    updates: list[Update] = Field(min_length=1)

    @pydantic.field_serializer("date")
    def serialize_date(
        self, date: dt.datetime, _info: pydantic.FieldSerializationInfo
    ) -> str:
        return str(date.strftime(INPUT_DATE_FORMAT))


class StatusPage(RootModel[Any]):
    """The root of the status page object, containing a list of incidents"""

    root: list[Incident]
