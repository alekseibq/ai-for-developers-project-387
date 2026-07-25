from app.domain.objects import MeetingTypeObj
from app.domain.result import Failure, Success
from app.repositories.meeting_type_repository import MeetingTypeRepository


class CreateMeetingTypeUseCase:
    def __init__(self, repo: MeetingTypeRepository) -> None:
        self._repo = repo

    async def __call__(
        self,
        name: str,
        description: str,
        duration_minutes: int,
    ) -> Success[MeetingTypeObj] | Failure:
        if not name or not name.strip():
            return Failure(error="Name is required", code="INVALID_NAME")
        if duration_minutes < 1:
            return Failure(error="Duration must be positive", code="INVALID_DURATION")

        meeting_type = await self._repo.create(
            name=name.strip(),
            description=description,
            duration_minutes=duration_minutes,
        )
        return Success(data=meeting_type)
