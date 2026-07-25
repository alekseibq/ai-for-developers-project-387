import os
import time

from app.domain.objects import HealthObj
from app.domain.result import Failure, Success
from app.repositories.health import HealthRepository

_start_time = time.time()


class HealthUseCase:
    def __init__(self, repo: HealthRepository):
        self._repo = repo

    async def __call__(self) -> Success[HealthObj] | Failure:
        try:
            database = await self._repo.check_database()
            obj = HealthObj(
                status="ok" if database == "connected" else "degraded",
                version=os.getenv("APP_VERSION", "0.1.0"),
                database=database,
                uptime=time.time() - _start_time,
            )
            return Success(data=obj)
        except Exception as exc:
            return Failure(error=str(exc), code="HEALTH_CHECK_FAILED")
