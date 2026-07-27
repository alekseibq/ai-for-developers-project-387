from datetime import UTC, datetime, timedelta

from app.domain.objects import BookingObj, SlotObj
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

    async def __call__(  # noqa: PLR0911
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

        if request_date.weekday() >= 5:  # noqa: PLR2004
            return Failure(error="Weekends are not available", code="OUTSIDE_WORK_HOURS")

        if any(h.date == request_date for h in meeting_type.holidays):
            return Failure(error="Date is a holiday", code="OUTSIDE_WORK_HOURS")

        tz = start_time.tzinfo
        day_date = start_time.date()
        work_start = datetime.combine(day_date, meeting_type.working_hours_start, tzinfo=tz)
        work_end = datetime.combine(day_date, meeting_type.working_hours_end, tzinfo=tz)
        if start_time < work_start or end_time > work_end:
            return Failure(error="Slot is outside working hours", code="OUTSIDE_WORK_HOURS")

        slot = SlotObj(start_time=start_time, end_time=end_time)
        for b in meeting_type.breaks:
            break_start = datetime.combine(start_time.date(), b.start_time, tzinfo=tz)
            break_end = datetime.combine(start_time.date(), b.end_time, tzinfo=tz)
            if slot.start_time < break_end and slot.end_time > break_start:
                return Failure(error="Slot overlaps with a break", code="OUTSIDE_WORK_HOURS")

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
