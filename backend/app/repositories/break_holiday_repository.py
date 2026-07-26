from datetime import date, time
from typing import Any

from bson import ObjectId

from app.domain.objects import BreakObj, HolidayObj
from app.infrastructure.database import Database


class BreakHolidayRepository:
    def __init__(self) -> None:
        self._breaks_collection = Database.get_db()["breaks"]
        self._holidays_collection = Database.get_db()["holidays"]

    async def find_all_breaks(self) -> list[BreakObj]:
        cursor = self._breaks_collection.find()
        result = []
        async for doc in cursor:
            result.append(self._doc_to_break(doc))
        return result

    async def find_all_holidays(self) -> list[HolidayObj]:
        cursor = self._holidays_collection.find()
        result = []
        async for doc in cursor:
            result.append(self._doc_to_holiday(doc))
        return result

    async def create_break(
        self,
        name: str,
        day_of_week: int,
        start_time: time,
        end_time: time,
    ) -> BreakObj:
        doc = {
            "name": name,
            "day_of_week": day_of_week,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        }
        result = await self._breaks_collection.insert_one(doc)
        return BreakObj(
            id=str(result.inserted_id),
            name=name,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
        )

    async def create_holiday(
        self,
        name: str,
        holiday_date: date,
    ) -> HolidayObj:
        doc = {
            "name": name,
            "date": holiday_date.isoformat(),
        }
        result = await self._holidays_collection.insert_one(doc)
        return HolidayObj(
            id=str(result.inserted_id),
            name=name,
            date=holiday_date,
        )

    async def delete_break(self, id: str) -> bool:
        result = await self._breaks_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    async def delete_holiday(self, id: str) -> bool:
        result = await self._holidays_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    def _doc_to_break(self, doc: dict[str, Any]) -> BreakObj:
        return BreakObj(
            id=str(doc["_id"]),
            name=doc["name"],
            day_of_week=doc["day_of_week"],
            start_time=time.fromisoformat(doc["start_time"]),
            end_time=time.fromisoformat(doc["end_time"]),
        )

    def _doc_to_holiday(self, doc: dict[str, Any]) -> HolidayObj:
        return HolidayObj(
            id=str(doc["_id"]),
            name=doc["name"],
            date=date.fromisoformat(doc["date"]),
        )
