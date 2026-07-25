from typing import Any

from bson import ObjectId

from app.domain.objects import MeetingTypeObj
from app.infrastructure.database import Database


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

    def _doc_to_obj(self, doc: dict[str, Any]) -> MeetingTypeObj:
        return MeetingTypeObj(
            id=str(doc["_id"]),
            name=doc["name"],
            description=doc["description"],
            duration_minutes=doc["duration_minutes"],
        )
