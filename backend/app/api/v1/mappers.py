from datetime import datetime

from app.api.v1.dto import BookingRawDto, BookingRichDto, MeetingTypeDto, SlotDto
from app.domain.objects import BookingObj, MeetingTypeObj, SlotObj


def meeting_type_obj_to_dto(obj: MeetingTypeObj) -> MeetingTypeDto:
    return MeetingTypeDto(
        id=obj.id,
        name=obj.name,
        description=obj.description,
        duration_minutes=obj.duration_minutes,
    )


def slot_obj_to_dto(obj: SlotObj) -> SlotDto:
    return SlotDto(start_time=obj.start_time, end_time=obj.end_time)


def booking_obj_to_raw_dto(obj: BookingObj) -> BookingRawDto:
    return BookingRawDto(
        id=obj.id,
        meeting_type_id=obj.meeting_type_id,
        guest_name=obj.guest_name,
        start_time=obj.start_time,
        created_at=obj.created_at,
    )


def booking_obj_to_rich_dto(
    obj: BookingObj,
    meeting_type: MeetingTypeObj,
    end_time: datetime,
) -> BookingRichDto:
    return BookingRichDto(
        id=obj.id,
        guest_name=obj.guest_name,
        start_time=obj.start_time,
        end_time=end_time,
        created_at=obj.created_at,
        meeting_type=meeting_type_obj_to_dto(meeting_type),
    )
