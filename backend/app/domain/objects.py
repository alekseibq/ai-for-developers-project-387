from datetime import date, datetime

from pydantic import BaseModel


class HealthObj(BaseModel):
    status: str
    version: str
    database: str
    uptime: float


class MeetingTypeObj(BaseModel):
    id: str
    name: str
    description: str
    duration_minutes: int


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
