from fastapi import APIRouter, Depends

from app.api.v1.dto import CreateMeetingTypeRequest, MeetingTypeDto, UpdateMeetingTypeRequest
from app.api.v1.mappers import meeting_type_obj_to_dto
from app.domain.result import Failure, Success
from app.infrastructure.di import (
    create_meeting_type_usecase,
    list_all_meeting_type_usecase,
    meeting_type_repository,
    update_meeting_type_usecase,
)
from app.repositories.meeting_type_repository import MeetingTypeRepository
from app.usecases.create_meeting_type_use_case import CreateMeetingTypeUseCase
from app.usecases.list_all_meeting_type_use_case import ListAllMeetingTypeUseCase
from app.usecases.update_meeting_type_use_case import UpdateMeetingTypeUseCase

router = APIRouter(tags=["meeting-types"])


@router.get("/api/v1/meeting-types")
async def get_meeting_types(
    use_case: ListAllMeetingTypeUseCase = Depends(list_all_meeting_type_usecase),
) -> Success[list[MeetingTypeDto]] | Failure:
    result = await use_case()
    if result.type == "failure":
        return result
    return Success(data=[meeting_type_obj_to_dto(t) for t in result.data])


@router.get("/api/v1/meeting-types/{id}")
async def get_meeting_type(
    id: str,
    repo: MeetingTypeRepository = Depends(meeting_type_repository),
) -> Success[MeetingTypeDto] | Failure:
    obj = await repo.find_by_id(id)
    if obj is None:
        return Failure(error="Meeting type not found", code="MEETING_TYPE_NOT_FOUND")
    return Success(data=meeting_type_obj_to_dto(obj))


@router.post("/api/v1/meeting-types")
async def create_meeting_type(
    body: CreateMeetingTypeRequest,
    use_case: CreateMeetingTypeUseCase = Depends(create_meeting_type_usecase),
) -> Success[MeetingTypeDto] | Failure:
    result = await use_case(
        name=body.name,
        description=body.description,
        duration_minutes=body.duration_minutes,
    )
    if result.type == "failure":
        return result
    return Success(data=meeting_type_obj_to_dto(result.data))


@router.patch("/api/v1/meeting-types/{id}")
async def update_meeting_type(
    id: str,
    body: UpdateMeetingTypeRequest,
    use_case: UpdateMeetingTypeUseCase = Depends(update_meeting_type_usecase),
) -> Success[MeetingTypeDto] | Failure:
    breaks = [b.model_dump() for b in body.breaks] if body.breaks is not None else None
    holidays = [h.model_dump() for h in body.holidays] if body.holidays is not None else None
    result = await use_case(
        id=id,
        name=body.name,
        description=body.description,
        duration_minutes=body.duration_minutes,
        working_hours_start=body.working_hours_start,
        working_hours_end=body.working_hours_end,
        breaks=breaks,
        holidays=holidays,
    )
    if result.type == "failure":
        return result
    return Success(data=meeting_type_obj_to_dto(result.data))
