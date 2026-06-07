from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
import fastf1
import redis.asyncio as redis

from src.cache import CacheService
from src.models import (
    HealthResponse,
    YearAvailabilityResponse,
    RaceNamesResponse,
    RaceScheduleResponse,
    SessionInfo,
)

cache_service: CacheService | None = None


async def get_cache() -> CacheService:
    return cache_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    global cache_service
    redis_client = await redis.from_url("redis://localhost")
    cache_service = CacheService(redis_client)
    yield
    await redis_client.aclose()


app = FastAPI(title="F1 Data API", version="0.1.0", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.get("/years/{year}/available", response_model=YearAvailabilityResponse)
async def check_year_availability(year: int):
    """Check if a given year has data available in FastF1."""
    try:
        fastf1.get_event(year, 1)
        has_data = True
    except (ValueError, KeyError):
        has_data = False

    return YearAvailabilityResponse(year=year, has_data=has_data)


@app.get("/years/{year}/races", response_model=RaceNamesResponse)
async def get_race_names(year: int, cache: CacheService = Depends(get_cache)):
    """Get all race/event names for a given year."""
    cache_key = f"f1:{year}:schedule"

    cached = await cache.get(cache_key)
    if cached:
        return RaceNamesResponse(year=year, races=cached["races"])

    try:
        schedule = fastf1.get_event_schedule(year)
        if schedule.empty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Year {year} not found in FastF1 data")
        races = schedule["EventName"].tolist()
    except (ValueError, KeyError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Year {year} not found in FastF1 data")

    await cache.set(cache_key, {"races": races})
    return RaceNamesResponse(year=year, races=races)


@app.get("/years/{year}/races/{race_name}/schedule", response_model=RaceScheduleResponse)
async def get_race_schedule(year: int, race_name: str, cache: CacheService = Depends(get_cache)):
    """Get event schedule (sessions) for a given year and race name."""
    cache_key = f"f1:{year}:{race_name}:schedule"

    cached = await cache.get(cache_key)
    if cached:
        sessions = [SessionInfo(**s) for s in cached["sessions"]]
        return RaceScheduleResponse(year=year, race_name=race_name, sessions=sessions)

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

    await cache.set(cache_key, {"sessions": [s.model_dump() for s in sessions]})
    return RaceScheduleResponse(year=year, race_name=race_name, sessions=sessions)
