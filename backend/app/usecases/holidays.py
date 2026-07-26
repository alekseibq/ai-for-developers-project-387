from datetime import date

from app.domain.objects import HolidayObj
from app.domain.result import Failure, Success
from app.repositories.break_holiday_repository import BreakHolidayRepository


class ListAllHolidaysUseCase:
    def __init__(self, repo: BreakHolidayRepository):
        self._repo = repo

    async def __call__(self) -> Success[list[HolidayObj]] | Failure:
        holidays = await self._repo.find_all_holidays()
        return Success(data=holidays)


class CreateHolidayUseCase:
    def __init__(self, repo: BreakHolidayRepository):
        self._repo = repo

    async def __call__(
        self,
        name: str,
        holiday_date: date,
    ) -> Success[HolidayObj] | Failure:
        if not name or not name.strip():
            return Failure(error="Name is required", code="INVALID_NAME")

        holiday = await self._repo.create_holiday(
            name=name.strip(),
            holiday_date=holiday_date,
        )
        return Success(data=holiday)


class DeleteHolidayUseCase:
    def __init__(self, repo: BreakHolidayRepository):
        self._repo = repo

    async def __call__(self, id: str) -> Success[None] | Failure:
        deleted = await self._repo.delete_holiday(id)
        if not deleted:
            return Failure(error="Holiday not found", code="NOT_FOUND")
        return Success(data=None)
