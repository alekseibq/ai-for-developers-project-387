from datetime import date, datetime

from pydantic import BaseModel


class BreakDto(BaseModel):
    start_time: str
    end_time: str


class HolidayDto(BaseModel):
    date: date
    name: str


class MeetingTypeDto(BaseModel):
    id: str
    name: str
    description: str
    duration_minutes: int
    working_hours_start: str = "09:00"
    working_hours_end: str = "18:00"
    breaks: list[BreakDto] = []
    holidays: list[HolidayDto] = []


class CreateMeetingTypeRequest(BaseModel):
    name: str
    description: str
    duration_minutes: int


class UpdateMeetingTypeRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    duration_minutes: int | None = None
    working_hours_start: str | None = None
    working_hours_end: str | None = None
    breaks: list[BreakDto] | None = None
    holidays: list[HolidayDto] | None = None


class SlotDto(BaseModel):
    start_time: datetime
    end_time: datetime


class BookingRawDto(BaseModel):
    id: str
    meeting_type_id: str
    guest_name: str
    start_time: datetime
    created_at: datetime


class BookingRichDto(BaseModel):
    id: str
    guest_name: str
    start_time: datetime
    end_time: datetime
    created_at: datetime
    meeting_type: MeetingTypeDto


class CreateBookingRequest(BaseModel):
    meeting_type_id: str
    guest_name: str
    start_time: datetime
