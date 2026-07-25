from unittest.mock import AsyncMock

import pytest

from app.domain.objects import MeetingTypeObj
from app.domain.result import Failure, Success
from app.usecases.create_meeting_type_use_case import CreateMeetingTypeUseCase


@pytest.fixture
def mock_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.create = AsyncMock(
        return_value=MeetingTypeObj(
            id="new_id",
            name="Consultation",
            description="A 30-min consultation",
            duration_minutes=30,
        )
    )
    return repo


@pytest.fixture
def use_case(mock_repo) -> CreateMeetingTypeUseCase:
    return CreateMeetingTypeUseCase(repo=mock_repo)


class TestCreateMeetingType:
    async def test_success(self, use_case: CreateMeetingTypeUseCase, mock_repo: AsyncMock):
        result = await use_case(
            name="Consultation",
            description="A 30-min consultation",
            duration_minutes=30,
        )

        assert isinstance(result, Success)
        assert isinstance(result.data, MeetingTypeObj)
        assert result.data.name == "Consultation"
        assert result.data.duration_minutes == 30
        mock_repo.create.assert_called_once_with(
            name="Consultation",
            description="A 30-min consultation",
            duration_minutes=30,
        )

    async def test_empty_name_fails(self, use_case: CreateMeetingTypeUseCase):
        result = await use_case(
            name="",
            description="Some desc",
            duration_minutes=30,
        )

        assert isinstance(result, Failure)
        assert result.code == "INVALID_NAME"

    async def test_blank_name_fails(self, use_case: CreateMeetingTypeUseCase):
        result = await use_case(
            name="   ",
            description="Some desc",
            duration_minutes=30,
        )

        assert isinstance(result, Failure)
        assert result.code == "INVALID_NAME"

    async def test_zero_duration_fails(self, use_case: CreateMeetingTypeUseCase):
        result = await use_case(
            name="Test",
            description="Some desc",
            duration_minutes=0,
        )

        assert isinstance(result, Failure)
        assert result.code == "INVALID_DURATION"

    async def test_negative_duration_fails(self, use_case: CreateMeetingTypeUseCase):
        result = await use_case(
            name="Test",
            description="Some desc",
            duration_minutes=-5,
        )

        assert isinstance(result, Failure)
        assert result.code == "INVALID_DURATION"
