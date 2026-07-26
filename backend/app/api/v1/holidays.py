from fastapi import APIRouter, Depends

from app.api.v1.dto import CreateHolidayRequest, HolidayDto
from app.api.v1.mappers import holiday_obj_to_dto
from app.domain.result import Failure, Success
from app.infrastructure.di import (
    create_holiday_usecase,
    delete_holiday_usecase,
    list_all_holidays_usecase,
)
from app.usecases.holidays import (
    CreateHolidayUseCase,
    DeleteHolidayUseCase,
    ListAllHolidaysUseCase,
)

router = APIRouter(tags=["holidays"])


@router.get("/api/v1/holidays")
async def get_holidays(
    use_case: ListAllHolidaysUseCase = Depends(list_all_holidays_usecase),
) -> Success[list[HolidayDto]] | Failure:
    result = await use_case()
    if result.type == "failure":
        return result
    return Success(data=[holiday_obj_to_dto(h) for h in result.data])


@router.post("/api/v1/holidays")
async def create_holiday(
    body: CreateHolidayRequest,
    use_case: CreateHolidayUseCase = Depends(create_holiday_usecase),
) -> Success[HolidayDto] | Failure:
    result = await use_case(
        name=body.name,
        holiday_date=body.date,
    )
    if result.type == "failure":
        return result
    return Success(data=holiday_obj_to_dto(result.data))


@router.delete("/api/v1/holidays/{holiday_id}")
async def delete_holiday(
    holiday_id: str,
    use_case: DeleteHolidayUseCase = Depends(delete_holiday_usecase),
) -> Success[None] | Failure:
    return await use_case(id=holiday_id)
