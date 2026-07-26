from datetime import date, time

import pytest

from app.domain.objects import BreakObj, HolidayObj
from app.repositories.break_holiday_repository import BreakHolidayRepository


@pytest.fixture
async def repo(db) -> BreakHolidayRepository:
    return BreakHolidayRepository()


class TestBreaks:
    async def test_find_all_breaks_empty(self, repo: BreakHolidayRepository):
        result = await repo.find_all_breaks()
        assert result == []

    async def test_create_and_find_break(self, repo: BreakHolidayRepository):
        created = await repo.create_break(
            name="Lunch",
            day_of_week=0,
            start_time=time(12, 0),
            end_time=time(13, 0),
        )

        assert isinstance(created, BreakObj)
        assert created.name == "Lunch"
        assert created.day_of_week == 0
        assert created.start_time == time(12, 0)
        assert created.end_time == time(13, 0)
        assert created.id is not None

        all_breaks = await repo.find_all_breaks()
        assert len(all_breaks) == 1
        assert all_breaks[0].name == "Lunch"

    async def test_delete_break(self, repo: BreakHolidayRepository):
        created = await repo.create_break(
            name="Lunch",
            day_of_week=0,
            start_time=time(12, 0),
            end_time=time(13, 0),
        )

        deleted = await repo.delete_break(created.id)
        assert deleted is True

        all_breaks = await repo.find_all_breaks()
        assert all_breaks == []

    async def test_delete_nonexistent_break(self, repo: BreakHolidayRepository):
        deleted = await repo.delete_break("000000000000000000000000")
        assert deleted is False


class TestHolidays:
    async def test_find_all_holidays_empty(self, repo: BreakHolidayRepository):
        result = await repo.find_all_holidays()
        assert result == []

    async def test_create_and_find_holiday(self, repo: BreakHolidayRepository):
        created = await repo.create_holiday(
            name="New Year",
            holiday_date=date(2027, 1, 1),
        )

        assert isinstance(created, HolidayObj)
        assert created.name == "New Year"
        assert created.date == date(2027, 1, 1)
        assert created.id is not None

        all_holidays = await repo.find_all_holidays()
        assert len(all_holidays) == 1
        assert all_holidays[0].name == "New Year"

    async def test_delete_holiday(self, repo: BreakHolidayRepository):
        created = await repo.create_holiday(
            name="New Year",
            holiday_date=date(2027, 1, 1),
        )

        deleted = await repo.delete_holiday(created.id)
        assert deleted is True

        all_holidays = await repo.find_all_holidays()
        assert all_holidays == []

    async def test_delete_nonexistent_holiday(self, repo: BreakHolidayRepository):
        deleted = await repo.delete_holiday("000000000000000000000000")
        assert deleted is False
