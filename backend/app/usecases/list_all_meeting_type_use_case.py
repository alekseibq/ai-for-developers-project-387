from app.domain.objects import MeetingTypeObj
from app.domain.result import Failure, Success
from app.repositories.meeting_type_repository import MeetingTypeRepository


class ListAllMeetingTypeUseCase:
    def __init__(self, repo: MeetingTypeRepository):
        self._repo = repo

    async def __call__(self) -> Success[list[MeetingTypeObj]] | Failure:
        types = await self._repo.find_all()
        return Success(data=types)
