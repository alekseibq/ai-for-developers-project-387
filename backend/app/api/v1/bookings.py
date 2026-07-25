from datetime import timedelta

from fastapi import APIRouter, Depends

from app.api.v1.dto import BookingRichDto, CreateBookingRequest
from app.api.v1.mappers import booking_obj_to_rich_dto
from app.domain.result import Failure, Success
from app.infrastructure.di import (
    create_booking_usecase,
    list_upcoming_bookings_usecase,
    meeting_type_repository,
)
from app.repositories.meeting_type_repository import MeetingTypeRepository
from app.usecases.create_booking_use_case import CreateBookingUseCase
from app.usecases.list_upcoming_bookings_use_case import ListUpcomingBookingsUseCase

router = APIRouter(tags=["bookings"])


@router.post("/api/v1/bookings")
async def create_booking(
    body: CreateBookingRequest,
    use_case: CreateBookingUseCase = Depends(create_booking_usecase),
    meeting_type_repo: MeetingTypeRepository = Depends(meeting_type_repository),
) -> Success[BookingRichDto] | Failure:
    result = await use_case(
        meeting_type_id=body.meeting_type_id,
        guest_name=body.guest_name,
        start_time=body.start_time,
    )
    if result.type == "failure":
        return result

    booking = result.data
    meeting_type = await meeting_type_repo.find_by_id(booking.meeting_type_id)
    if not meeting_type:
        return Failure(error="Meeting type not found", code="MEETING_TYPE_NOT_FOUND")

    end_time = booking.start_time + timedelta(minutes=meeting_type.duration_minutes)
    return Success(data=booking_obj_to_rich_dto(booking, meeting_type, end_time))


@router.get("/api/v1/bookings")
async def list_bookings(
    use_case: ListUpcomingBookingsUseCase = Depends(list_upcoming_bookings_usecase),
    meeting_type_repo: MeetingTypeRepository = Depends(meeting_type_repository),
) -> Success[list[BookingRichDto]] | Failure:
    result = await use_case()
    if result.type == "failure":
        return result

    bookings = result.data
    type_ids = list({b.meeting_type_id for b in bookings})
    types = await meeting_type_repo.find_by_ids(type_ids)
    type_map = {t.id: t for t in types}

    dto_list = []
    for b in bookings:
        mt = type_map.get(b.meeting_type_id)
        if mt is None:
            continue
        end_time = b.start_time + timedelta(minutes=mt.duration_minutes)
        dto_list.append(booking_obj_to_rich_dto(b, mt, end_time))

    return Success(data=dto_list)
