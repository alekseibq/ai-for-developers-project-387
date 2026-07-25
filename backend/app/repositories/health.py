from app.infrastructure.database import Database


class HealthRepository:
    async def check_database(self) -> str:
        try:
            is_connected = await Database.ping()
            return "connected" if is_connected else "disconnected"
        except Exception:
            return "disconnected"
