from fastapi import FastAPI, HTTPException, status
import fastf1

from src.models import (
    HealthResponse,
    YearAvailabilityResponse,
    RaceNamesResponse,
    RaceScheduleResponse,
    SessionInfo,
)

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


@app.get("/years/{year}/races", response_model=RaceNamesResponse)
def get_race_names(year: int):
    """Get all race/event names for a given year."""
    try:
        schedule = fastf1.get_event_schedule(year)
        if schedule.empty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Year {year} not found in FastF1 data")
        races = schedule["EventName"].tolist()
    except (ValueError, KeyError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Year {year} not found in FastF1 data")

    return RaceNamesResponse(year=year, races=races)


@app.get("/years/{year}/races/{race_name}/schedule", response_model=RaceScheduleResponse)
def get_race_schedule(year: int, race_name: str):
    """Get event schedule (sessions) for a given year and race name."""
    try:
        schedule = fastf1.get_event_schedule(year)
        event_row = schedule[schedule["EventName"] == race_name]
        if event_row.empty:
            raise ValueError(f"Race '{race_name}' not found for year {year}")

        event = fastf1.get_event(year, int(event_row.iloc[0]["RoundNumber"]))
    except (ValueError, KeyError, IndexError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Race '{race_name}' not found for year {year}"
        )

    sessions = []
    for i in range(1, 6):
        session_name = event.get(f"Session{i}")
        session_date_utc = event.get(f"Session{i}DateUtc")
        if session_name and session_date_utc:
            sessions.append(SessionInfo(name=session_name, date_utc=session_date_utc))

    return RaceScheduleResponse(year=year, race_name=race_name, sessions=sessions)
