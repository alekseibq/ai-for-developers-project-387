from datetime import date
from unittest.mock import AsyncMock

import pytest

from app.domain.objects import HolidayObj
from app.domain.result import Failure, Success
from app.usecases.holidays import CreateHolidayUseCase, DeleteHolidayUseCase, ListAllHolidaysUseCase


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock()


class TestListAllHolidays:
    async def test_returns_list_of_holidays(self, mock_repo: AsyncMock):
        holidays = [
            HolidayObj(id="h1", name="New Year", date=date(2027, 1, 1)),
        ]
        mock_repo.find_all_holidays = AsyncMock(return_value=holidays)

        use_case = ListAllHolidaysUseCase(repo=mock_repo)
        result = await use_case()

        assert isinstance(result, Success)
        assert len(result.data) == 1
        assert result.data[0].name == "New Year"

    async def test_returns_empty_list(self, mock_repo: AsyncMock):
        mock_repo.find_all_holidays = AsyncMock(return_value=[])

        use_case = ListAllHolidaysUseCase(repo=mock_repo)
        result = await use_case()

        assert isinstance(result, Success)
        assert result.data == []


class TestCreateHoliday:
    async def test_success(self, mock_repo: AsyncMock):
        mock_repo.create_holiday = AsyncMock(
            return_value=HolidayObj(id="h1", name="New Year", date=date(2027, 1, 1)),
        )

        use_case = CreateHolidayUseCase(repo=mock_repo)
        result = await use_case(name="New Year", holiday_date=date(2027, 1, 1))

        assert isinstance(result, Success)
        assert result.data.name == "New Year"

    async def test_empty_name_fails(self, mock_repo: AsyncMock):
        use_case = CreateHolidayUseCase(repo=mock_repo)
        result = await use_case(name="", holiday_date=date(2027, 1, 1))

        assert isinstance(result, Failure)
        assert result.code == "INVALID_NAME"


class TestDeleteHoliday:
    async def test_success(self, mock_repo: AsyncMock):
        mock_repo.delete_holiday = AsyncMock(return_value=True)

        use_case = DeleteHolidayUseCase(repo=mock_repo)
        result = await use_case(id="h1")

        assert isinstance(result, Success)

    async def test_not_found_fails(self, mock_repo: AsyncMock):
        mock_repo.delete_holiday = AsyncMock(return_value=False)

        use_case = DeleteHolidayUseCase(repo=mock_repo)
        result = await use_case(id="nonexistent")

        assert isinstance(result, Failure)
        assert result.code == "NOT_FOUND"
