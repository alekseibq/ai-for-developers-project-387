from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.domain.objects import BookingObj, MeetingTypeObj
from app.domain.result import Failure, Success
from app.usecases.create_booking_use_case import CreateBookingUseCase

_NOW = datetime.now(UTC)
TODAY = _NOW.replace(hour=0, minute=0, second=0, microsecond=0)
IN_WINDOW = TODAY + timedelta(days=1)


@pytest.fixture
def mock_booking_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.find_overlapping = AsyncMock(return_value=[])
    repo.create = AsyncMock(
        return_value=BookingObj(
            id="booking1",
            meeting_type_id="mt1",
            guest_name="John Doe",
            start_time=IN_WINDOW.replace(hour=10, minute=0),
            created_at=TODAY,
        )
    )
    return repo


@pytest.fixture
def mock_meeting_type_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.find_by_id = AsyncMock(
        return_value=MeetingTypeObj(
            id="mt1",
            name="Consultation",
            description="30-min consultation",
            duration_minutes=30,
        )
    )
    return repo


@pytest.fixture
def use_case(mock_booking_repo, mock_meeting_type_repo) -> CreateBookingUseCase:
    return CreateBookingUseCase(
        booking_repo=mock_booking_repo,
        meeting_type_repo=mock_meeting_type_repo,
    )


class TestCreateBooking:
    async def test_success(self, use_case: CreateBookingUseCase, mock_booking_repo: AsyncMock):
        result = await use_case(
            meeting_type_id="mt1",
            guest_name="John Doe",
            start_time=IN_WINDOW.replace(hour=10, minute=0),
        )

        assert isinstance(result, Success)
        assert isinstance(result.data, BookingObj)
        assert result.data.guest_name == "John Doe"
        mock_booking_repo.create.assert_called_once()

    async def test_empty_guest_name_fails(self, use_case: CreateBookingUseCase):
        result = await use_case(
            meeting_type_id="mt1",
            guest_name="",
            start_time=IN_WINDOW.replace(hour=10, minute=0),
        )

        assert isinstance(result, Failure)
        assert result.code == "INVALID_GUEST_NAME"

    async def test_blank_guest_name_fails(self, use_case: CreateBookingUseCase):
        result = await use_case(
            meeting_type_id="mt1",
            guest_name="   ",
            start_time=IN_WINDOW.replace(hour=10, minute=0),
        )

        assert isinstance(result, Failure)
        assert result.code == "INVALID_GUEST_NAME"

    async def test_meeting_type_not_found_fails(
        self,
        use_case: CreateBookingUseCase,
        mock_meeting_type_repo: AsyncMock,
    ):
        mock_meeting_type_repo.find_by_id = AsyncMock(return_value=None)

        result = await use_case(
            meeting_type_id="nonexistent",
            guest_name="John Doe",
            start_time=IN_WINDOW.replace(hour=10, minute=0),
        )

        assert isinstance(result, Failure)
        assert result.code == "MEETING_TYPE_NOT_FOUND"

    async def test_start_time_before_working_hours_fails(self, use_case: CreateBookingUseCase):
        result = await use_case(
            meeting_type_id="mt1",
            guest_name="John Doe",
            start_time=IN_WINDOW.replace(hour=7, minute=0),
        )

        assert isinstance(result, Failure)
        assert result.code == "OUTSIDE_WORK_HOURS"

    async def test_end_time_after_working_hours_fails(self, use_case: CreateBookingUseCase):
        result = await use_case(
            meeting_type_id="mt1",
            guest_name="John Doe",
            start_time=IN_WINDOW.replace(hour=17, minute=45),
        )

        assert isinstance(result, Failure)
        assert result.code == "OUTSIDE_WORK_HOURS"

    async def test_date_before_today_fails(self, use_case: CreateBookingUseCase):
        yesterday = datetime.now(UTC) - timedelta(days=1)

        result = await use_case(
            meeting_type_id="mt1",
            guest_name="John Doe",
            start_time=yesterday,
        )

        assert isinstance(result, Failure)
        assert result.code == "OUTSIDE_BOOKING_WINDOW"

    async def test_date_after_booking_window_fails(self, use_case: CreateBookingUseCase):
        result = await use_case(
            meeting_type_id="mt1",
            guest_name="John Doe",
            start_time=(IN_WINDOW + timedelta(days=14)).replace(hour=10, minute=0),
        )

        assert isinstance(result, Failure)
        assert result.code == "OUTSIDE_BOOKING_WINDOW"

    async def test_overlapping_slot_fails(
        self,
        use_case: CreateBookingUseCase,
        mock_booking_repo: AsyncMock,
    ):
        mock_booking_repo.find_overlapping = AsyncMock(
            return_value=[
                BookingObj(
                    id="existing",
                    meeting_type_id="mt1",
                    guest_name="Jane",
                    start_time=IN_WINDOW.replace(hour=10, minute=0),
                    created_at=TODAY,
                ),
            ]
        )

        result = await use_case(
            meeting_type_id="mt1",
            guest_name="John Doe",
            start_time=IN_WINDOW.replace(hour=10, minute=0),
        )

        assert isinstance(result, Failure)
        assert result.code == "SLOT_TAKEN"
