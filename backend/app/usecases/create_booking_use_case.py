from datetime import UTC, datetime, time, timedelta

from app.domain.objects import BookingObj
from app.domain.result import Failure, Success
from app.repositories.booking_repository import BookingRepository
from app.repositories.meeting_type_repository import MeetingTypeRepository


class CreateBookingUseCase:
    def __init__(
        self,
        booking_repo: BookingRepository,
        meeting_type_repo: MeetingTypeRepository,
    ):
        self._booking_repo = booking_repo
        self._meeting_type_repo = meeting_type_repo

    async def __call__(
        self,
        meeting_type_id: str,
        guest_name: str,
        start_time: datetime,
    ) -> Success[BookingObj] | Failure:
        if not guest_name or not guest_name.strip():
            return Failure(error="Guest name is required", code="INVALID_GUEST_NAME")

        meeting_type = await self._meeting_type_repo.find_by_id(meeting_type_id)
        if not meeting_type:
            return Failure(error="Meeting type not found", code="MEETING_TYPE_NOT_FOUND")

        duration = timedelta(minutes=meeting_type.duration_minutes)
        end_time = start_time + duration

        today = datetime.now(UTC).date()
        request_date = start_time.date()
        if request_date < today or request_date > today + timedelta(days=13):
            return Failure(error="Date is outside booking window", code="OUTSIDE_BOOKING_WINDOW")

        tz = start_time.tzinfo
        work_start = datetime.combine(start_time.date(), time(9, 0), tzinfo=tz)
        work_end = datetime.combine(start_time.date(), time(18, 0), tzinfo=tz)
        if start_time < work_start or end_time > work_end:
            return Failure(error="Slot is outside working hours", code="OUTSIDE_WORK_HOURS")

        overlapping = await self._booking_repo.find_overlapping(start_time, end_time)
        if overlapping:
            return Failure(error="Slot is already booked", code="SLOT_TAKEN")

        booking = await self._booking_repo.create(
            meeting_type_id=meeting_type_id,
            guest_name=guest_name.strip(),
            start_time=start_time,
            end_time=end_time,
        )
        return Success(data=booking)
