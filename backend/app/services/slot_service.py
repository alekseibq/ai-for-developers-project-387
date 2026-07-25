from datetime import date, datetime, time, timedelta

from app.domain.objects import MeetingTypeObj, SlotObj
from app.repositories.booking_repository import BookingRepository


class SlotService:
    def __init__(self, booking_repo: BookingRepository):
        self._booking_repo = booking_repo

    async def find_available_slots(
        self,
        day: date,
        meeting_type: MeetingTypeObj,
    ) -> list[SlotObj]:
        if day.weekday() >= 5:  # noqa: PLR2004
            return []

        day_start = datetime.combine(day, time.min)
        day_end = datetime.combine(day, time.max)
        occupied = await self._booking_repo.find_occupied_intervals(day_start, day_end)

        work_start = datetime.combine(day, time(9, 0))
        work_end = datetime.combine(day, time(18, 0))
        duration = timedelta(minutes=meeting_type.duration_minutes)

        candidates: list[SlotObj] = []
        cursor = work_start
        while cursor + duration <= work_end:
            slot = SlotObj(start_time=cursor, end_time=cursor + duration)
            if not self._overlaps(slot, occupied):
                candidates.append(slot)
            cursor += duration

        return candidates

    def _overlaps(
        self,
        slot: SlotObj,
        occupied: list[tuple[datetime, datetime]],
    ) -> bool:
        for occ_start, occ_end in occupied:
            if slot.start_time < occ_end and slot.end_time > occ_start:
                return True
        return False
