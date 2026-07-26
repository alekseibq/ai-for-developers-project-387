from datetime import date, datetime, time

from pydantic import BaseModel


class HealthObj(BaseModel):
    status: str
    version: str
    database: str
    uptime: float


class BreakObj(BaseModel):
    start_time: time
    end_time: time


class HolidayObj(BaseModel):
    date: date
    name: str


class MeetingTypeObj(BaseModel):
    id: str
    name: str
    description: str
    duration_minutes: int
    working_hours_start: time = time(9, 0)
    working_hours_end: time = time(18, 0)
    breaks: list[BreakObj] = []
    holidays: list[HolidayObj] = []


class SlotObj(BaseModel):
    start_time: datetime
    end_time: datetime


class BookingObj(BaseModel):
    id: str
    meeting_type_id: str
    guest_name: str
    start_time: datetime
    created_at: datetime


class SlotDateRangeObj(BaseModel):
    min_date: date
    max_date: date
