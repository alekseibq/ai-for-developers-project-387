from datetime import date, datetime, time, timedelta

from app.domain.objects import MeetingTypeObj, SlotObj
from app.repositories.booking_repository import BookingRepository
from app.repositories.break_holiday_repository import BreakHolidayRepository


class SlotService:
    def __init__(
        self,
        booking_repo: BookingRepository,
        break_holiday_repo: BreakHolidayRepository,
    ):
        self._booking_repo = booking_repo
        self._break_holiday_repo = break_holiday_repo

    async def find_available_slots(
        self,
        day: date,
        meeting_type: MeetingTypeObj,
    ) -> list[SlotObj]:
        if day.weekday() >= 5:  # noqa: PLR2004
            return []

        holidays = await self._break_holiday_repo.find_all_holidays()
        for h in holidays:
            if h.date == day:
                return []

        breaks = await self._break_holiday_repo.find_all_breaks()

        day_start = datetime.combine(day, time.min)
        day_end = datetime.combine(day, time.max)
        occupied = await self._booking_repo.find_occupied_intervals(day_start, day_end)

        break_intervals: list[tuple[datetime, datetime]] = []
        for b in breaks:
            if b.day_of_week != -1 and b.day_of_week != day.weekday():
                continue
            break_start = datetime.combine(day, b.start_time)
            break_end = datetime.combine(day, b.end_time)
            break_intervals.append((break_start, break_end))

        work_start = datetime.combine(day, time(9, 0))
        work_end = datetime.combine(day, time(18, 0))
        duration = timedelta(minutes=meeting_type.duration_minutes)

        candidates: list[SlotObj] = []
        cursor = work_start
        while cursor + duration <= work_end:
            slot = SlotObj(start_time=cursor, end_time=cursor + duration)
            if not self._overlaps(slot, occupied) and not self._overlaps(slot, break_intervals):
                candidates.append(slot)
            cursor += duration

        return candidates

    def _overlaps(
        self,
        slot: SlotObj,
        intervals: list[tuple[datetime, datetime]],
    ) -> bool:
        for int_start, int_end in intervals:
            if slot.start_time < int_end and slot.end_time > int_start:
                return True
        return False
