from datetime import datetime
from pydantic import BaseModel, Field


class SessionInfo(BaseModel):
    name: str = Field(description="Session name (e.g., 'Practice 1', 'Qualifying', 'Race')")
    date_utc: datetime = Field(description="Session date and time in UTC")


class RaceScheduleResponse(BaseModel):
    year: int
    race_name: str
    sessions: list[SessionInfo]


class RaceNamesResponse(BaseModel):
    year: int
    races: list[str] = Field(description="List of race/event names for the year")
