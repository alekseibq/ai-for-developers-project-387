from unittest.mock import AsyncMock

import pytest

from app.domain.objects import MeetingTypeObj
from app.domain.result import Success
from app.usecases.list_all_meeting_type_use_case import ListAllMeetingTypeUseCase


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def use_case(mock_repo: AsyncMock) -> ListAllMeetingTypeUseCase:
    return ListAllMeetingTypeUseCase(repo=mock_repo)


class TestListAllMeetingType:
    async def test_returns_list_of_types(
        self,
        use_case: ListAllMeetingTypeUseCase,
        mock_repo: AsyncMock,
    ):
        types = [
            MeetingTypeObj(id="1", name="Type A", description="A", duration_minutes=30),
            MeetingTypeObj(id="2", name="Type B", description="B", duration_minutes=60),
        ]
        mock_repo.find_all = AsyncMock(return_value=types)

        result = await use_case()

        assert isinstance(result, Success)
        assert result.data == types
        assert len(result.data) == 2

    async def test_returns_empty_list_when_no_types(
        self,
        use_case: ListAllMeetingTypeUseCase,
        mock_repo: AsyncMock,
    ):
        mock_repo.find_all = AsyncMock(return_value=[])

        result = await use_case()

        assert isinstance(result, Success)
        assert result.data == []
