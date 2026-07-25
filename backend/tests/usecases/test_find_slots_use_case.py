from datetime import date, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.domain.objects import MeetingTypeObj, SlotDateRangeObj, SlotObj
from app.domain.result import Failure, Success
from app.usecases.find_slots_use_case import FindSlotsUseCase

TODAY = date(2026, 6, 15)


@pytest.fixture
def mock_slot_service() -> AsyncMock:
    service = AsyncMock()
    service.find_available_slots = AsyncMock(
        return_value=[
            SlotObj(start_time=datetime(2026, 6, 15, 9, 0), end_time=datetime(2026, 6, 15, 9, 30)),
            SlotObj(start_time=datetime(2026, 6, 15, 9, 30), end_time=datetime(2026, 6, 15, 10, 0)),
        ]
    )
    return service


@pytest.fixture
def mock_propose_dates() -> AsyncMock:
    service = AsyncMock()
    service.return_value = SlotDateRangeObj(
        min_date=TODAY,
        max_date=TODAY + timedelta(days=13),
    )
    return service


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
def use_case(mock_slot_service, mock_propose_dates, mock_meeting_type_repo) -> FindSlotsUseCase:
    return FindSlotsUseCase(
        slot_service=mock_slot_service,
        propose_dates_service=mock_propose_dates,
        meeting_type_repo=mock_meeting_type_repo,
    )


class TestFindSlots:
    async def test_success(self, use_case: FindSlotsUseCase):
        result = await use_case(date_str="2026-06-15", meeting_type_id="mt1")

        assert isinstance(result, Success)
        assert len(result.data) == 2

    async def test_invalid_date_format_fails(self, use_case: FindSlotsUseCase):
        result = await use_case(date_str="invalid-date", meeting_type_id="mt1")

        assert isinstance(result, Failure)
        assert result.code == "INVALID_DATE"

    async def test_wrong_date_format_fails(self, use_case: FindSlotsUseCase):
        result = await use_case(date_str="15-06-2026", meeting_type_id="mt1")

        assert isinstance(result, Failure)
        assert result.code == "INVALID_DATE"

    async def test_date_before_min_date_fails(
        self,
        use_case: FindSlotsUseCase,
        mock_propose_dates: AsyncMock,
    ):
        mock_propose_dates.return_value = SlotDateRangeObj(
            min_date=TODAY,
            max_date=TODAY + timedelta(days=13),
        )

        result = await use_case(date_str="2026-06-14", meeting_type_id="mt1")

        assert isinstance(result, Failure)
        assert result.code == "OUTSIDE_BOOKING_WINDOW"

    async def test_date_after_max_date_fails(
        self,
        use_case: FindSlotsUseCase,
        mock_propose_dates: AsyncMock,
    ):
        mock_propose_dates.return_value = SlotDateRangeObj(
            min_date=TODAY,
            max_date=TODAY + timedelta(days=13),
        )

        result = await use_case(date_str="2026-06-29", meeting_type_id="mt1")

        assert isinstance(result, Failure)
        assert result.code == "OUTSIDE_BOOKING_WINDOW"

    async def test_meeting_type_not_found_fails(
        self,
        use_case: FindSlotsUseCase,
        mock_meeting_type_repo: AsyncMock,
    ):
        mock_meeting_type_repo.find_by_id = AsyncMock(return_value=None)

        result = await use_case(date_str="2026-06-15", meeting_type_id="nonexistent")

        assert isinstance(result, Failure)
        assert result.code == "MEETING_TYPE_NOT_FOUND"

    async def test_calls_slot_service_with_correct_args(
        self,
        use_case: FindSlotsUseCase,
        mock_slot_service: AsyncMock,
        mock_meeting_type_repo: AsyncMock,
    ):
        expected_meeting_type = MeetingTypeObj(
            id="mt1",
            name="Consultation",
            description="30-min consultation",
            duration_minutes=30,
        )

        await use_case(date_str="2026-06-15", meeting_type_id="mt1")

        mock_slot_service.find_available_slots.assert_called_once_with(
            date(2026, 6, 15),
            expected_meeting_type,
        )
