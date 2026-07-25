from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.bookings import router as bookings_router
from app.api.v1.health import router as health_router
from app.api.v1.meeting_types import router as meeting_types_router
from app.api.v1.slots import router as slots_router
from app.infrastructure.database import Database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await Database.connect()
    yield
    await Database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.api_route("/", methods=["GET", "HEAD"])
async def root() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(meeting_types_router)
app.include_router(slots_router)
app.include_router(bookings_router)
