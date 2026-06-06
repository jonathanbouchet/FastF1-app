from fastapi import FastAPI
import fastf1

from src.models import HealthResponse, YearAvailabilityResponse

app = FastAPI(title="F1 Data API", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.get("/years/{year}/available", response_model=YearAvailabilityResponse)
def check_year_availability(year: int):
    """Check if a given year has data available in FastF1."""
    try:
        fastf1.get_event(year, 1)
        has_data = True
    except (ValueError, KeyError):
        has_data = False

    return YearAvailabilityResponse(year=year, has_data=has_data)
