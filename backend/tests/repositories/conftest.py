import os

import pytest_asyncio

from app.infrastructure.database import Database
from app.repositories.booking_repository import BookingRepository
from app.repositories.meeting_type_repository import MeetingTypeRepository


@pytest_asyncio.fixture
async def db(mongodb_container):
    uri = mongodb_container.get_connection_url()
    os.environ["MONGO_URI"] = uri
    await Database.connect()
    collection_names = await Database.get_db().list_collection_names()
    for name in collection_names:
        await Database.get_db()[name].delete_many({})
    yield
    await Database.disconnect()


@pytest_asyncio.fixture
async def meeting_type_repo(db):
    return MeetingTypeRepository()


@pytest_asyncio.fixture
async def booking_repo(db):
    return BookingRepository()
