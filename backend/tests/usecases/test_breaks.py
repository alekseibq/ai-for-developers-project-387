from datetime import time
from unittest.mock import AsyncMock

import pytest

from app.domain.objects import BreakObj
from app.domain.result import Failure, Success
from app.usecases.breaks import CreateBreakUseCase, DeleteBreakUseCase, ListAllBreaksUseCase


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock()


class TestListAllBreaks:
    async def test_returns_list_of_breaks(self, mock_repo: AsyncMock):
        breaks = [
            BreakObj(id="b1", name="Lunch", day_of_week=0, start_time=time(12, 0), end_time=time(13, 0)),
        ]
        mock_repo.find_all_breaks = AsyncMock(return_value=breaks)

        use_case = ListAllBreaksUseCase(repo=mock_repo)
        result = await use_case()

        assert isinstance(result, Success)
        assert len(result.data) == 1
        assert result.data[0].name == "Lunch"

    async def test_returns_empty_list(self, mock_repo: AsyncMock):
        mock_repo.find_all_breaks = AsyncMock(return_value=[])

        use_case = ListAllBreaksUseCase(repo=mock_repo)
        result = await use_case()

        assert isinstance(result, Success)
        assert result.data == []


class TestCreateBreak:
    async def test_success(self, mock_repo: AsyncMock):
        mock_repo.create_break = AsyncMock(
            return_value=BreakObj(id="b1", name="Lunch", day_of_week=0, start_time=time(12, 0), end_time=time(13, 0)),
        )

        use_case = CreateBreakUseCase(repo=mock_repo)
        result = await use_case(name="Lunch", day_of_week=0, start_time=time(12, 0), end_time=time(13, 0))

        assert isinstance(result, Success)
        assert result.data.name == "Lunch"

    async def test_empty_name_fails(self, mock_repo: AsyncMock):
        use_case = CreateBreakUseCase(repo=mock_repo)
        result = await use_case(name="", day_of_week=0, start_time=time(12, 0), end_time=time(13, 0))

        assert isinstance(result, Failure)
        assert result.code == "INVALID_NAME"

    async def test_invalid_day_of_week_fails(self, mock_repo: AsyncMock):
        use_case = CreateBreakUseCase(repo=mock_repo)
        result = await use_case(name="Lunch", day_of_week=7, start_time=time(12, 0), end_time=time(13, 0))

        assert isinstance(result, Failure)
        assert result.code == "INVALID_DAY_OF_WEEK"

    async def test_start_time_after_end_time_fails(self, mock_repo: AsyncMock):
        use_case = CreateBreakUseCase(repo=mock_repo)
        result = await use_case(name="Lunch", day_of_week=0, start_time=time(14, 0), end_time=time(13, 0))

        assert isinstance(result, Failure)
        assert result.code == "INVALID_TIME_RANGE"

    async def test_start_time_equal_end_time_fails(self, mock_repo: AsyncMock):
        use_case = CreateBreakUseCase(repo=mock_repo)
        result = await use_case(name="Lunch", day_of_week=0, start_time=time(13, 0), end_time=time(13, 0))

        assert isinstance(result, Failure)
        assert result.code == "INVALID_TIME_RANGE"


class TestDeleteBreak:
    async def test_success(self, mock_repo: AsyncMock):
        mock_repo.delete_break = AsyncMock(return_value=True)

        use_case = DeleteBreakUseCase(repo=mock_repo)
        result = await use_case(id="b1")

        assert isinstance(result, Success)

    async def test_not_found_fails(self, mock_repo: AsyncMock):
        mock_repo.delete_break = AsyncMock(return_value=False)

        use_case = DeleteBreakUseCase(repo=mock_repo)
        result = await use_case(id="nonexistent")

        assert isinstance(result, Failure)
        assert result.code == "NOT_FOUND"
