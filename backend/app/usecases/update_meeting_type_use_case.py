from app.domain.objects import MeetingTypeObj
from app.domain.result import Failure, Success
from app.repositories.meeting_type_repository import MeetingTypeRepository


class UpdateMeetingTypeUseCase:
    def __init__(self, repo: MeetingTypeRepository) -> None:
        self._repo = repo

    async def __call__(  # noqa: PLR0913, PLR0917
        self,
        id: str,
        name: str | None = None,
        description: str | None = None,
        duration_minutes: int | None = None,
        working_hours_start: str | None = None,
        working_hours_end: str | None = None,
        breaks: list[dict[str, str]] | None = None,
        holidays: list[dict[str, str]] | None = None,
    ) -> Success[MeetingTypeObj] | Failure:
        existing = await self._repo.find_by_id(id)
        if not existing:
            return Failure(error="Meeting type not found", code="MEETING_TYPE_NOT_FOUND")

        if name is not None and not name.strip():
            return Failure(error="Name is required", code="INVALID_NAME")
        if duration_minutes is not None and duration_minutes < 1:
            return Failure(error="Duration must be positive", code="INVALID_DURATION")

        meeting_type = await self._repo.update(
            id=id,
            name=name.strip() if name else None,
            description=description,
            duration_minutes=duration_minutes,
            working_hours_start=working_hours_start,
            working_hours_end=working_hours_end,
            breaks=breaks,
            holidays=holidays,
        )
        if not meeting_type:
            return Failure(error="Meeting type not found", code="MEETING_TYPE_NOT_FOUND")
        return Success(data=meeting_type)
