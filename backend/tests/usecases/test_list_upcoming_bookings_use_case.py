from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.domain.objects import BookingObj
from app.domain.result import Success
from app.usecases.list_upcoming_bookings_use_case import ListUpcomingBookingsUseCase

TODAY = datetime(2026, 6, 15)


@pytest.fixture
def mock_booking_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def use_case(mock_booking_repo: AsyncMock) -> ListUpcomingBookingsUseCase:
    return ListUpcomingBookingsUseCase(booking_repo=mock_booking_repo)


class TestListUpcomingBookings:
    async def test_returns_list_of_bookings(
        self,
        use_case: ListUpcomingBookingsUseCase,
        mock_booking_repo: AsyncMock,
    ):
        bookings = [
            BookingObj(
                id="b1",
                meeting_type_id="mt1",
                guest_name="John",
                start_time=datetime(2026, 6, 16, 10, 0),
                created_at=TODAY,
            ),
            BookingObj(
                id="b2",
                meeting_type_id="mt1",
                guest_name="Jane",
                start_time=datetime(2026, 6, 17, 14, 0),
                created_at=TODAY,
            ),
        ]
        mock_booking_repo.find_all_upcoming = AsyncMock(return_value=bookings)

        result = await use_case()

        assert isinstance(result, Success)
        assert result.data == bookings
        assert len(result.data) == 2

    async def test_returns_empty_list_when_no_bookings(
        self,
        use_case: ListUpcomingBookingsUseCase,
        mock_booking_repo: AsyncMock,
    ):
        mock_booking_repo.find_all_upcoming = AsyncMock(return_value=[])

        result = await use_case()

        assert isinstance(result, Success)
        assert result.data == []
