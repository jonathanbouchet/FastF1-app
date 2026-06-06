from pydantic import BaseModel, Field


class YearAvailabilityResponse(BaseModel):
    year: int
    has_data: bool = Field(description="Whether the given year has F1 data in FastF1")
