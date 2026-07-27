from typing import Any

from bson import ObjectId

from app.domain.objects import BreakObj, HolidayObj, MeetingTypeObj
from app.infrastructure.database import Database


def _parse_time(value: Any) -> str:
    if isinstance(value, str):
        return value
    return value.strftime("%H:%M")  # type: ignore[no-any-return]


class MeetingTypeRepository:
    def __init__(self) -> None:
        self._collection = Database.get_db()["meeting_types"]

    async def find_all(self) -> list[MeetingTypeObj]:
        cursor = self._collection.find()
        result = []
        async for doc in cursor:
            result.append(self._doc_to_obj(doc))
        return result

    async def find_by_id(self, id: str) -> MeetingTypeObj | None:
        doc = await self._collection.find_one({"_id": ObjectId(id)})
        if doc is None:
            return None
        return self._doc_to_obj(doc)

    async def find_by_ids(self, ids: list[str]) -> list[MeetingTypeObj]:
        object_ids = [ObjectId(id) for id in ids]
        cursor = self._collection.find({"_id": {"$in": object_ids}})
        result = []
        async for doc in cursor:
            result.append(self._doc_to_obj(doc))
        return result

    async def create(
        self,
        name: str,
        description: str,
        duration_minutes: int,
    ) -> MeetingTypeObj:
        doc = {
            "name": name,
            "description": description,
            "duration_minutes": duration_minutes,
        }
        result = await self._collection.insert_one(doc)
        return MeetingTypeObj(
            id=str(result.inserted_id),
            name=name,
            description=description,
            duration_minutes=duration_minutes,
        )

    async def update(  # noqa: PLR0913
        self,
        id: str,
        name: str | None = None,
        description: str | None = None,
        duration_minutes: int | None = None,
        working_hours_start: str | None = None,
        working_hours_end: str | None = None,
        breaks: list[dict[str, str]] | None = None,
        holidays: list[dict[str, str]] | None = None,
    ) -> MeetingTypeObj | None:
        update: dict[str, Any] = {}
        if name is not None:
            update["name"] = name
        if description is not None:
            update["description"] = description
        if duration_minutes is not None:
            update["duration_minutes"] = duration_minutes
        if working_hours_start is not None:
            update["working_hours_start"] = working_hours_start
        if working_hours_end is not None:
            update["working_hours_end"] = working_hours_end
        if breaks is not None:
            update["breaks"] = breaks
        if holidays is not None:
            update["holidays"] = holidays

        if not update:
            return await self.find_by_id(id)

        result = await self._collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update},
            return_document=True,
        )
        if result is None:
            return None
        return self._doc_to_obj(result)

    def _doc_to_obj(self, doc: dict[str, Any]) -> MeetingTypeObj:
        raw_breaks = doc.get("breaks", [])
        breaks = [
            BreakObj(start_time=b["start_time"], end_time=b["end_time"])
            for b in raw_breaks
        ]
        raw_holidays = doc.get("holidays", [])
        holidays = [
            HolidayObj(date=h["date"], name=h.get("name", ""))
            for h in raw_holidays
        ]
        return MeetingTypeObj(
            id=str(doc["_id"]),
            name=doc["name"],
            description=doc["description"],
            duration_minutes=doc["duration_minutes"],
            working_hours_start=_parse_time(doc.get("working_hours_start", "09:00")),
            working_hours_end=_parse_time(doc.get("working_hours_end", "18:00")),
            breaks=breaks,
            holidays=holidays,
        )
