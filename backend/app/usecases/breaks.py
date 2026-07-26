from datetime import time

from app.domain.objects import BreakObj
from app.domain.result import Failure, Success
from app.repositories.break_holiday_repository import BreakHolidayRepository


class ListAllBreaksUseCase:
    def __init__(self, repo: BreakHolidayRepository):
        self._repo = repo

    async def __call__(self) -> Success[list[BreakObj]] | Failure:
        breaks = await self._repo.find_all_breaks()
        return Success(data=breaks)


class CreateBreakUseCase:
    def __init__(self, repo: BreakHolidayRepository):
        self._repo = repo

    async def __call__(
        self,
        name: str,
        day_of_week: int,
        start_time: time,
        end_time: time,
    ) -> Success[BreakObj] | Failure:
        if not name or not name.strip():
            return Failure(error="Name is required", code="INVALID_NAME")
        if day_of_week < 0 or day_of_week > 6:
            return Failure(error="Day of week must be 0-6", code="INVALID_DAY_OF_WEEK")
        if start_time >= end_time:
            return Failure(error="Start time must be before end time", code="INVALID_TIME_RANGE")

        break_obj = await self._repo.create_break(
            name=name.strip(),
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
        )
        return Success(data=break_obj)


class DeleteBreakUseCase:
    def __init__(self, repo: BreakHolidayRepository):
        self._repo = repo

    async def __call__(self, id: str) -> Success[None] | Failure:
        deleted = await self._repo.delete_break(id)
        if not deleted:
            return Failure(error="Break not found", code="NOT_FOUND")
        return Success(data=None)
