from datetime import date, datetime, time, timedelta
from unittest.mock import AsyncMock

import pytest

from app.domain.objects import BreakObj, HolidayObj, MeetingTypeObj
from app.services.slot_service import SlotService


@pytest.fixture
def meeting_type_30min() -> MeetingTypeObj:
    return MeetingTypeObj(
        id="mt1",
        name="Test Meeting",
        description="Test",
        duration_minutes=30,
    )


@pytest.fixture
def meeting_type_60min() -> MeetingTypeObj:
    return MeetingTypeObj(
        id="mt2",
        name="Long Meeting",
        description="Long",
        duration_minutes=60,
    )


@pytest.fixture
def meeting_type_90min() -> MeetingTypeObj:
    return MeetingTypeObj(
        id="mt3",
        name="Extra Long",
        description="Extra long",
        duration_minutes=90,
    )


@pytest.fixture
def mock_booking_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.find_occupied_intervals = AsyncMock(return_value=[])
    return repo


@pytest.fixture
def mock_break_holiday_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.find_all_breaks = AsyncMock(return_value=[])
    repo.find_all_holidays = AsyncMock(return_value=[])
    return repo


@pytest.fixture
def service(mock_booking_repo, mock_break_holiday_repo) -> SlotService:
    return SlotService(
        booking_repo=mock_booking_repo,
        break_holiday_repo=mock_break_holiday_repo,
    )


class TestFindAvailableSlots:
    async def test_weekday_returns_30min_slots_in_working_hours(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
        mock_booking_repo: AsyncMock,
    ):
        monday = date(2026, 6, 15)

        slots = await service.find_available_slots(monday, meeting_type_30min)

        assert len(slots) == 18
        for i, slot in enumerate(slots):
            expected_start = datetime(2026, 6, 15, 9, 0) + i * timedelta(minutes=30)
            expected_end = expected_start + timedelta(minutes=30)
            assert slot.start_time == expected_start
            assert slot.end_time == expected_end

    async def test_weekend_returns_empty(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
    ):
        saturday = date(2026, 6, 13)
        sunday = date(2026, 6, 14)

        sat_slots = await service.find_available_slots(saturday, meeting_type_30min)
        sun_slots = await service.find_available_slots(sunday, meeting_type_30min)

        assert sat_slots == []
        assert sun_slots == []

    async def test_with_60min_duration_produces_half_slots(
        self,
        service: SlotService,
        meeting_type_60min: MeetingTypeObj,
    ):
        monday = date(2026, 6, 15)

        slots = await service.find_available_slots(monday, meeting_type_60min)

        assert len(slots) == 9
        for i, slot in enumerate(slots):
            expected_start = datetime(2026, 6, 15, 9, 0) + i * timedelta(minutes=60)
            expected_end = expected_start + timedelta(minutes=60)
            assert slot.start_time == expected_start
            assert slot.end_time == expected_end

    async def test_90min_duration_produces_6_slots(
        self,
        service: SlotService,
        meeting_type_90min: MeetingTypeObj,
    ):
        monday = date(2026, 6, 15)

        slots = await service.find_available_slots(monday, meeting_type_90min)

        assert len(slots) == 6
        assert slots[0].start_time == datetime(2026, 6, 15, 9, 0)
        assert slots[0].end_time == datetime(2026, 6, 15, 10, 30)
        assert slots[-1].start_time == datetime(2026, 6, 15, 16, 30)
        assert slots[-1].end_time == datetime(2026, 6, 15, 18, 0)

    async def test_slot_that_ends_exactly_at_18_00_is_included(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
    ):
        monday = date(2026, 6, 15)

        slots = await service.find_available_slots(monday, meeting_type_30min)

        last_slot = slots[-1]
        assert last_slot.start_time == datetime(2026, 6, 15, 17, 30)
        assert last_slot.end_time == datetime(2026, 6, 15, 18, 0)

    async def test_overlapping_slots_are_excluded(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
        mock_booking_repo: AsyncMock,
    ):
        monday = date(2026, 6, 15)
        occupied = [
            (datetime(2026, 6, 15, 10, 0), datetime(2026, 6, 15, 11, 0)),
        ]
        mock_booking_repo.find_occupied_intervals = AsyncMock(return_value=occupied)

        slots = await service.find_available_slots(monday, meeting_type_30min)

        assert len(slots) == 16
        for slot in slots:
            assert slot.start_time not in (
                datetime(2026, 6, 15, 10, 0),
                datetime(2026, 6, 15, 10, 30),
            )

    async def test_occupied_intervals_correctly_passed_to_repo(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
        mock_booking_repo: AsyncMock,
    ):
        monday = date(2026, 6, 15)

        await service.find_available_slots(monday, meeting_type_30min)

        expected_day_start = datetime(2026, 6, 15, 0, 0)
        expected_day_end = datetime(2026, 6, 15, 23, 59, 59, 999999)
        mock_booking_repo.find_occupied_intervals.assert_called_once_with(
            expected_day_start,
            expected_day_end,
        )

    async def test_partial_overlap_excludes_slot(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
        mock_booking_repo: AsyncMock,
    ):
        monday = date(2026, 6, 15)
        occupied = [
            (datetime(2026, 6, 15, 10, 15), datetime(2026, 6, 15, 10, 45)),
        ]
        mock_booking_repo.find_occupied_intervals = AsyncMock(return_value=occupied)

        slots = await service.find_available_slots(monday, meeting_type_30min)

        assert len(slots) == 16
        slot_starts = {s.start_time for s in slots}
        assert datetime(2026, 6, 15, 10, 0) not in slot_starts
        assert datetime(2026, 6, 15, 10, 30) not in slot_starts

    async def test_no_slots_when_full_day_occupied(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
        mock_booking_repo: AsyncMock,
    ):
        monday = date(2026, 6, 15)
        occupied = [
            (datetime(2026, 6, 15, 9, 0), datetime(2026, 6, 15, 18, 0)),
        ]
        mock_booking_repo.find_occupied_intervals = AsyncMock(return_value=occupied)

        slots = await service.find_available_slots(monday, meeting_type_30min)

        assert slots == []

    async def test_multiple_occupied_intervals(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
        mock_booking_repo: AsyncMock,
    ):
        monday = date(2026, 6, 15)
        occupied = [
            (datetime(2026, 6, 15, 10, 0), datetime(2026, 6, 15, 10, 30)),
            (datetime(2026, 6, 15, 13, 0), datetime(2026, 6, 15, 14, 0)),
            (datetime(2026, 6, 15, 15, 30), datetime(2026, 6, 15, 16, 0)),
        ]
        mock_booking_repo.find_occupied_intervals = AsyncMock(return_value=occupied)

        slots = await service.find_available_slots(monday, meeting_type_30min)

        assert len(slots) == 14

    async def test_holiday_returns_empty(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
        mock_break_holiday_repo: AsyncMock,
    ):
        monday = date(2026, 6, 15)
        mock_break_holiday_repo.find_all_holidays = AsyncMock(
            return_value=[HolidayObj(id="h1", name="Test Holiday", date=monday)],
        )

        slots = await service.find_available_slots(monday, meeting_type_30min)

        assert slots == []

    async def test_break_excludes_slots(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
        mock_break_holiday_repo: AsyncMock,
    ):
        monday = date(2026, 6, 15)
        mock_break_holiday_repo.find_all_breaks = AsyncMock(
            return_value=[BreakObj(id="b1", name="Lunch", day_of_week=0, start_time=time(12, 0), end_time=time(13, 0))],
        )

        slots = await service.find_available_slots(monday, meeting_type_30min)

        assert len(slots) == 16
        for slot in slots:
            slot_start_hour = slot.start_time.hour
            assert slot_start_hour < 12 or slot_start_hour >= 13

    async def test_break_on_different_day_does_not_affect(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
        mock_break_holiday_repo: AsyncMock,
    ):
        monday = date(2026, 6, 15)
        mock_break_holiday_repo.find_all_breaks = AsyncMock(
            return_value=[BreakObj(id="b1", name="Weekend", day_of_week=6, start_time=time(12, 0), end_time=time(13, 0))],
        )

        slots = await service.find_available_slots(monday, meeting_type_30min)

        assert len(slots) == 18

    async def test_holiday_on_different_date_does_not_affect(
        self,
        service: SlotService,
        meeting_type_30min: MeetingTypeObj,
        mock_break_holiday_repo: AsyncMock,
    ):
        monday = date(2026, 6, 15)
        mock_break_holiday_repo.find_all_holidays = AsyncMock(
            return_value=[HolidayObj(id="h1", name="Future Holiday", date=date(2026, 7, 1))],
        )

        slots = await service.find_available_slots(monday, meeting_type_30min)

        assert len(slots) == 18
