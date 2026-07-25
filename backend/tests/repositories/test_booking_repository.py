from datetime import datetime, timedelta

import pytest

from app.domain.objects import BookingObj, MeetingTypeObj


@pytest.fixture
async def meeting_type(meeting_type_repo) -> MeetingTypeObj:
    return await meeting_type_repo.create(
        name="Consultation",
        description="30 min",
        duration_minutes=30,
    )


TODAY = datetime(2026, 6, 15)


class TestCreate:
    async def test_returns_booking_with_id(self, booking_repo, meeting_type):
        start = datetime(2026, 6, 15, 10, 0)
        end = datetime(2026, 6, 15, 10, 30)

        result = await booking_repo.create(
            meeting_type_id=meeting_type.id,
            guest_name="John Doe",
            start_time=start,
            end_time=end,
        )

        assert isinstance(result, BookingObj)
        assert result.id is not None
        assert len(result.id) == 24
        assert result.meeting_type_id == meeting_type.id
        assert result.guest_name == "John Doe"
        assert result.start_time == start
        assert result.created_at is not None


class TestFindOccupiedIntervals:
    async def test_empty_when_no_bookings(self, booking_repo):
        day_start = datetime(2026, 6, 15, 0, 0)
        day_end = datetime(2026, 6, 15, 23, 59)

        result = await booking_repo.find_occupied_intervals(day_start, day_end)

        assert result == []

    async def test_returns_intervals(self, booking_repo, meeting_type):
        await booking_repo.create(
            meeting_type_id=meeting_type.id,
            guest_name="John",
            start_time=datetime(2026, 6, 15, 10, 0),
            end_time=datetime(2026, 6, 15, 10, 30),
        )

        day_start = datetime(2026, 6, 15, 0, 0)
        day_end = datetime(2026, 6, 15, 23, 59)

        result = await booking_repo.find_occupied_intervals(day_start, day_end)

        assert len(result) == 1
        start, end = result[0]
        assert start == datetime(2026, 6, 15, 10, 0)
        assert end == datetime(2026, 6, 15, 10, 30)

    async def test_outside_day_range(self, booking_repo, meeting_type):
        await booking_repo.create(
            meeting_type_id=meeting_type.id,
            guest_name="John",
            start_time=datetime(2026, 6, 16, 10, 0),
            end_time=datetime(2026, 6, 16, 10, 30),
        )

        day_start = datetime(2026, 6, 15, 0, 0)
        day_end = datetime(2026, 6, 15, 23, 59)

        result = await booking_repo.find_occupied_intervals(day_start, day_end)

        assert result == []


class TestFindOverlapping:
    async def test_exact_overlap(self, booking_repo, meeting_type):
        await booking_repo.create(
            meeting_type_id=meeting_type.id,
            guest_name="John",
            start_time=datetime(2026, 6, 15, 10, 0),
            end_time=datetime(2026, 6, 15, 10, 30),
        )

        result = await booking_repo.find_overlapping(
            datetime(2026, 6, 15, 10, 0),
            datetime(2026, 6, 15, 10, 30),
        )

        assert len(result) == 1
        assert result[0].guest_name == "John"

    async def test_partial_overlap(self, booking_repo, meeting_type):
        await booking_repo.create(
            meeting_type_id=meeting_type.id,
            guest_name="John",
            start_time=datetime(2026, 6, 15, 10, 0),
            end_time=datetime(2026, 6, 15, 10, 30),
        )

        result = await booking_repo.find_overlapping(
            datetime(2026, 6, 15, 10, 15),
            datetime(2026, 6, 15, 10, 45),
        )

        assert len(result) == 1

    async def test_no_overlap(self, booking_repo, meeting_type):
        await booking_repo.create(
            meeting_type_id=meeting_type.id,
            guest_name="John",
            start_time=datetime(2026, 6, 15, 10, 0),
            end_time=datetime(2026, 6, 15, 10, 30),
        )

        result = await booking_repo.find_overlapping(
            datetime(2026, 6, 15, 11, 0),
            datetime(2026, 6, 15, 11, 30),
        )

        assert result == []


class TestFindAllUpcoming:
    async def test_returns_future_bookings(self, booking_repo, meeting_type):
        future_start = datetime.utcnow() + timedelta(days=1)

        await booking_repo.create(
            meeting_type_id=meeting_type.id,
            guest_name="John",
            start_time=future_start,
            end_time=future_start + timedelta(minutes=30),
        )

        result = await booking_repo.find_all_upcoming()

        assert len(result) == 1
        assert result[0].guest_name == "John"

    async def test_excludes_past_bookings(self, booking_repo, meeting_type):
        past_start = datetime.utcnow() - timedelta(days=1)

        await booking_repo.create(
            meeting_type_id=meeting_type.id,
            guest_name="Old",
            start_time=past_start,
            end_time=past_start + timedelta(minutes=30),
        )

        result = await booking_repo.find_all_upcoming()

        assert result == []

    async def test_returns_sorted_by_start_time(self, booking_repo, meeting_type):
        later = datetime.utcnow() + timedelta(days=2, hours=11)
        earlier = datetime.utcnow() + timedelta(days=2, hours=10)

        await booking_repo.create(
            meeting_type_id=meeting_type.id,
            guest_name="Later",
            start_time=later,
            end_time=later + timedelta(minutes=30),
        )
        await booking_repo.create(
            meeting_type_id=meeting_type.id,
            guest_name="Earlier",
            start_time=earlier,
            end_time=earlier + timedelta(minutes=30),
        )

        result = await booking_repo.find_all_upcoming()

        assert len(result) == 2
        assert result[0].guest_name == "Earlier"
        assert result[1].guest_name == "Later"
