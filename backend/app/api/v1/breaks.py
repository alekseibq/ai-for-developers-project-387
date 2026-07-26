from fastapi import APIRouter, Depends

from app.api.v1.dto import BreakDto, CreateBreakRequest
from app.api.v1.mappers import break_obj_to_dto
from app.domain.result import Failure, Success
from app.infrastructure.di import (
    create_break_usecase,
    delete_break_usecase,
    list_all_breaks_usecase,
)
from app.usecases.breaks import CreateBreakUseCase, DeleteBreakUseCase, ListAllBreaksUseCase

router = APIRouter(tags=["breaks"])


@router.get("/api/v1/breaks")
async def get_breaks(
    use_case: ListAllBreaksUseCase = Depends(list_all_breaks_usecase),
) -> Success[list[BreakDto]] | Failure:
    result = await use_case()
    if result.type == "failure":
        return result
    return Success(data=[break_obj_to_dto(b) for b in result.data])


@router.post("/api/v1/breaks")
async def create_break(
    body: CreateBreakRequest,
    use_case: CreateBreakUseCase = Depends(create_break_usecase),
) -> Success[BreakDto] | Failure:
    result = await use_case(
        name=body.name,
        day_of_week=body.day_of_week,
        start_time=body.start_time,
        end_time=body.end_time,
    )
    if result.type == "failure":
        return result
    return Success(data=break_obj_to_dto(result.data))


@router.delete("/api/v1/breaks/{break_id}")
async def delete_break(
    break_id: str,
    use_case: DeleteBreakUseCase = Depends(delete_break_usecase),
) -> Success[None] | Failure:
    return await use_case(id=break_id)
