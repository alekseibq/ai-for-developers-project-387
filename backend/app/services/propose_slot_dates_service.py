from datetime import datetime, timedelta

from app.domain.objects import SlotDateRangeObj


class ProposeSlotDatesService:
    async def __call__(self) -> SlotDateRangeObj:
        today = datetime.utcnow().date()
        return SlotDateRangeObj(
            min_date=today,
            max_date=today + timedelta(days=13),
        )
