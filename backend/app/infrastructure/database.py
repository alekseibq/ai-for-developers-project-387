import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class Database:
    _client: AsyncIOMotorClient | None = None  # type: ignore[type-arg]
    _db: AsyncIOMotorDatabase | None = None  # type: ignore[type-arg]

    @classmethod
    async def connect(cls) -> None:
        uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/calcom")
        db_name = os.getenv("MONGO_DB_NAME", "calcom")
        cls._client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        cls._db = cls._client[db_name]

    @classmethod
    async def disconnect(cls) -> None:
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:  # type: ignore[type-arg]
        if cls._db is None:
            raise RuntimeError("Database not connected")
        return cls._db

    @classmethod
    async def ping(cls) -> bool:
        try:
            await cls.get_db().command("ping")
            return True
        except Exception:
            return False
