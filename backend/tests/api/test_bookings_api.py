from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

from app.domain.result import Failure
from app.infrastructure.di import (
    create_booking_usecase,
    list_upcoming_bookings_usecase,
    meeting_type_repository,
)
from app.main import app
from app.repositories.booking_repository import BookingRepository
from app.repositories.meeting_type_repository import MeetingTypeRepository
from app.usecases.create_booking_use_case import CreateBookingUseCase

TODAY = datetime.now(UTC)


class TestCreateBooking:
    async def _create_meeting_type(self, test_client, name="Consultation", duration=30):
        resp = await test_client.post(
            "/api/v1/meeting-types",
            json={
                "name": name,
                "description": "test",
                "duration_minutes": duration,
            },
        )
        return resp.json()["data"]["id"]

    async def test_success(self, test_client):
        mt_id = await self._create_meeting_type(test_client)
        start = _next_weekday_10am(TODAY)

        response = await test_client.post(
            "/api/v1/bookings",
            json={
                "meeting_type_id": mt_id,
                "guest_name": "John Doe",
                "start_time": start.isoformat(),
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert body["data"]["guest_name"] == "John Doe"
        assert "id" in body["data"]
        assert "meeting_type" in body["data"]

    async def test_empty_guest_name_fails(self, test_client):
        mt_id = await self._create_meeting_type(test_client)
        start = _next_weekday_10am(TODAY)

        response = await test_client.post(
            "/api/v1/bookings",
            json={
                "meeting_type_id": mt_id,
                "guest_name": "",
                "start_time": start.isoformat(),
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "failure"
        assert body["code"] == "INVALID_GUEST_NAME"

    async def test_nonexistent_meeting_type_fails(self, test_client):
        start = _next_weekday_10am(TODAY)

        response = await test_client.post(
            "/api/v1/bookings",
            json={
                "meeting_type_id": "000000000000000000000000",
                "guest_name": "John Doe",
                "start_time": start.isoformat(),
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "failure"
        assert body["code"] == "MEETING_TYPE_NOT_FOUND"

    async def test_outside_working_hours_fails(self, test_client):
        mt_id = await self._create_meeting_type(test_client)
        start = _next_weekday_8am(TODAY)

        response = await test_client.post(
            "/api/v1/bookings",
            json={
                "meeting_type_id": mt_id,
                "guest_name": "John Doe",
                "start_time": start.isoformat(),
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "failure"
        assert body["code"] == "OUTSIDE_WORK_HOURS"

    async def test_meeting_type_not_found_after_booking_created(self, test_client):
        mt_id = await self._create_meeting_type(test_client)
        start = _next_weekday_10am(TODAY)

        real_booking_repo = BookingRepository()
        real_mt_repo = MeetingTypeRepository()
        real_use_case = CreateBookingUseCase(
            booking_repo=real_booking_repo,
            meeting_type_repo=real_mt_repo,
        )

        mock_mt_repo = AsyncMock(spec=MeetingTypeRepository)
        mock_mt_repo.find_by_id = AsyncMock(return_value=None)

        app.dependency_overrides[create_booking_usecase] = lambda: real_use_case
        app.dependency_overrides[meeting_type_repository] = lambda: mock_mt_repo

        try:
            response = await test_client.post(
                "/api/v1/bookings",
                json={
                    "meeting_type_id": mt_id,
                    "guest_name": "John Doe",
                    "start_time": start.isoformat(),
                },
            )

            assert response.status_code == 200
            body = response.json()
            assert body["type"] == "failure"
            assert body["code"] == "MEETING_TYPE_NOT_FOUND"
        finally:
            app.dependency_overrides.clear()

    async def test_slot_taken_fails(self, test_client):
        mt_id = await self._create_meeting_type(test_client)
        start = _next_weekday_10am(TODAY)

        await test_client.post(
            "/api/v1/bookings",
            json={
                "meeting_type_id": mt_id,
                "guest_name": "First",
                "start_time": start.isoformat(),
            },
        )

        response = await test_client.post(
            "/api/v1/bookings",
            json={
                "meeting_type_id": mt_id,
                "guest_name": "Second",
                "start_time": start.isoformat(),
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "failure"
        assert body["code"] == "SLOT_TAKEN"


class TestListBookings:
    async def _create_meeting_type(self, test_client, name="Consultation", duration=30):
        resp = await test_client.post(
            "/api/v1/meeting-types",
            json={
                "name": name,
                "description": "test",
                "duration_minutes": duration,
            },
        )
        return resp.json()["data"]["id"]

    async def test_empty_list(self, test_client):
        response = await test_client.get("/api/v1/bookings")

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert body["data"] == []

    async def test_returns_upcoming_bookings(self, test_client):
        mt_id = await self._create_meeting_type(test_client)
        start = _next_weekday_10am(TODAY)

        await test_client.post(
            "/api/v1/bookings",
            json={
                "meeting_type_id": mt_id,
                "guest_name": "John Doe",
                "start_time": start.isoformat(),
            },
        )

        response = await test_client.get("/api/v1/bookings")

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert len(body["data"]) >= 1
        assert body["data"][0]["guest_name"] == "John Doe"

    async def test_returns_failure_when_usecase_fails(self, test_client):
        mock_usecase = AsyncMock()
        mock_usecase.return_value = Failure(error="DB error", code="DB_ERROR")

        app.dependency_overrides[list_upcoming_bookings_usecase] = lambda: mock_usecase

        try:
            response = await test_client.get("/api/v1/bookings")

            assert response.status_code == 200
            body = response.json()
            assert body["type"] == "failure"
            assert body["code"] == "DB_ERROR"
        finally:
            app.dependency_overrides.clear()

    async def test_skip_booking_without_meeting_type(self, test_client):
        repo = BookingRepository()
        future = datetime.now(UTC) + timedelta(days=1, hours=10)
        await repo.create(
            meeting_type_id="000000000000000000000000",
            guest_name="Orphan Booking",
            start_time=future,
            end_time=future + timedelta(minutes=30),
        )

        response = await test_client.get("/api/v1/bookings")

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert body["data"] == []


def _next_weekday_10am(d: datetime) -> datetime:
    for i in range(1, 8):
        candidate = d + timedelta(days=i)
        if candidate.weekday() < 5:
            return candidate.replace(hour=10, minute=0, second=0, microsecond=0)
    return d


def _next_weekday_8am(d: datetime) -> datetime:
    for i in range(1, 8):
        candidate = d + timedelta(days=i)
        if candidate.weekday() < 5:
            return candidate.replace(hour=8, minute=0, second=0, microsecond=0)
    return d
