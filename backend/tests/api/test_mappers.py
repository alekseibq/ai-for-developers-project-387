from datetime import datetime

from app.api.v1.dto import BookingRichDto, MeetingTypeDto, SlotDto
from app.api.v1.mappers import (
    booking_obj_to_raw_dto,
    booking_obj_to_rich_dto,
    meeting_type_obj_to_dto,
    slot_obj_to_dto,
)
from app.domain.objects import BookingObj, MeetingTypeObj, SlotObj


def test_meeting_type_obj_to_dto():
    obj = MeetingTypeObj(
        id="mt1",
        name="Consultation",
        description="30-min meeting",
        duration_minutes=30,
    )

    dto = meeting_type_obj_to_dto(obj)

    assert isinstance(dto, MeetingTypeDto)
    assert dto.id == "mt1"
    assert dto.name == "Consultation"
    assert dto.description == "30-min meeting"
    assert dto.duration_minutes == 30


def test_slot_obj_to_dto():
    obj = SlotObj(
        start_time=datetime(2026, 6, 15, 9, 0),
        end_time=datetime(2026, 6, 15, 9, 30),
    )

    dto = slot_obj_to_dto(obj)

    assert isinstance(dto, SlotDto)
    assert dto.start_time == datetime(2026, 6, 15, 9, 0)
    assert dto.end_time == datetime(2026, 6, 15, 9, 30)


def test_booking_obj_to_raw_dto():
    obj = BookingObj(
        id="b1",
        meeting_type_id="mt1",
        guest_name="John Doe",
        start_time=datetime(2026, 6, 15, 10, 0),
        created_at=datetime(2026, 6, 15, 8, 0),
    )

    dto = booking_obj_to_raw_dto(obj)

    assert dto.id == "b1"
    assert dto.meeting_type_id == "mt1"
    assert dto.guest_name == "John Doe"
    assert dto.start_time == datetime(2026, 6, 15, 10, 0)
    assert dto.created_at == datetime(2026, 6, 15, 8, 0)


def test_booking_obj_to_rich_dto():
    booking = BookingObj(
        id="b1",
        meeting_type_id="mt1",
        guest_name="John Doe",
        start_time=datetime(2026, 6, 15, 10, 0),
        created_at=datetime(2026, 6, 15, 8, 0),
    )
    meeting_type = MeetingTypeObj(
        id="mt1",
        name="Consultation",
        description="30-min meeting",
        duration_minutes=30,
    )
    end_time = datetime(2026, 6, 15, 10, 30)

    dto = booking_obj_to_rich_dto(booking, meeting_type, end_time)

    assert isinstance(dto, BookingRichDto)
    assert dto.id == "b1"
    assert dto.guest_name == "John Doe"
    assert dto.start_time == datetime(2026, 6, 15, 10, 0)
    assert dto.end_time == datetime(2026, 6, 15, 10, 30)
    assert dto.created_at == datetime(2026, 6, 15, 8, 0)
    assert dto.meeting_type.id == "mt1"
    assert dto.meeting_type.name == "Consultation"
