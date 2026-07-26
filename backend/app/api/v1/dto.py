from datetime import date, datetime, time

from pydantic import BaseModel


class MeetingTypeDto(BaseModel):
    id: str
    name: str
    description: str
    duration_minutes: int


class CreateMeetingTypeRequest(BaseModel):
    name: str
    description: str
    duration_minutes: int


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


class BreakDto(BaseModel):
    id: str
    name: str
    day_of_week: int
    start_time: time
    end_time: time


class CreateBreakRequest(BaseModel):
    name: str
    day_of_week: int
    start_time: time
    end_time: time


class HolidayDto(BaseModel):
    id: str
    name: str
    date: date


class CreateHolidayRequest(BaseModel):
    name: str
    date: date
