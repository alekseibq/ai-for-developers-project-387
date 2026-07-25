from datetime import UTC, datetime
from typing import Any

from app.domain.objects import BookingObj
from app.infrastructure.database import Database


class BookingRepository:
    def __init__(self) -> None:
        self._collection = Database.get_db()["bookings"]

    async def create(
        self,
        meeting_type_id: str,
        guest_name: str,
        start_time: datetime,
        end_time: datetime,
    ) -> BookingObj:
        doc: dict[str, Any] = {
            "meeting_type_id": meeting_type_id,
            "guest_name": guest_name,
            "start_time": start_time,
            "end_time": end_time,
            "created_at": datetime.now(UTC),
        }
        result = await self._collection.insert_one(doc)
        return BookingObj(
            id=str(result.inserted_id),
            meeting_type_id=meeting_type_id,
            guest_name=guest_name,
            start_time=start_time,
            created_at=doc["created_at"],
        )

    async def find_occupied_intervals(
        self,
        day_start: datetime,
        day_end: datetime,
    ) -> list[tuple[datetime, datetime]]:
        cursor = self._collection.find(
            {"start_time": {"$lt": day_end}, "end_time": {"$gt": day_start}},
            {"start_time": 1, "end_time": 1},
        )
        result: list[tuple[datetime, datetime]] = []
        async for doc in cursor:
            result.append((doc["start_time"], doc["end_time"]))
        return result

    async def find_overlapping(
        self,
        start: datetime,
        end: datetime,
    ) -> list[BookingObj]:
        cursor = self._collection.find(
            {"start_time": {"$lt": end}, "end_time": {"$gt": start}},
        )
        result = []
        async for doc in cursor:
            result.append(self._doc_to_obj(doc))
        return result

    async def find_all_upcoming(self) -> list[BookingObj]:
        now = datetime.now(UTC)
        cursor = self._collection.find(
            {"start_time": {"$gt": now}},
        ).sort("start_time", 1)
        result = []
        async for doc in cursor:
            result.append(self._doc_to_obj(doc))
        return result

    def _doc_to_obj(self, doc: dict[str, Any]) -> BookingObj:
        return BookingObj(
            id=str(doc["_id"]),
            meeting_type_id=doc["meeting_type_id"],
            guest_name=doc["guest_name"],
            start_time=doc["start_time"],
            created_at=doc["created_at"],
        )
