from unittest.mock import patch

from app.infrastructure.database import Database
from app.repositories.health import HealthRepository


class TestHealthRepository:
    async def test_check_database_connected(self, db):
        repo = HealthRepository()

        result = await repo.check_database()

        assert result == "connected"

    async def test_check_database_returns_disconnected_on_ping_exception(self, db):
        repo = HealthRepository()
        with patch.object(Database, "ping", side_effect=Exception("Connection refused")):
            result = await repo.check_database()

        assert result == "disconnected"
