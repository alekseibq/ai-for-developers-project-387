from fastapi import APIRouter, Depends, Query

from app.api.v1.dto import SlotDto
from app.api.v1.mappers import slot_obj_to_dto
from app.domain.result import Failure, Success
from app.infrastructure.di import find_slots_usecase
from app.usecases.find_slots_use_case import FindSlotsUseCase

router = APIRouter(tags=["slots"])


@router.get("/api/v1/slots")
async def get_slots(
    date: str = Query(description="Date in YYYY-MM-DD format"),
    meeting_type_id: str = Query(description="Meeting type ID"),
    use_case: FindSlotsUseCase = Depends(find_slots_usecase),
) -> Success[list[SlotDto]] | Failure:
    result = await use_case(date_str=date, meeting_type_id=meeting_type_id)
    if result.type == "failure":
        return result
    return Success(data=[slot_obj_to_dto(s) for s in result.data])
