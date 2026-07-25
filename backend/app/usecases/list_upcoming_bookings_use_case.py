from app.domain.objects import BookingObj
from app.domain.result import Failure, Success
from app.repositories.booking_repository import BookingRepository


class ListUpcomingBookingsUseCase:
    def __init__(self, booking_repo: BookingRepository):
        self._booking_repo = booking_repo

    async def __call__(self) -> Success[list[BookingObj]] | Failure:
        bookings = await self._booking_repo.find_all_upcoming()
        return Success(data=bookings)
