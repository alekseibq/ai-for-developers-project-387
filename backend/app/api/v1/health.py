from fastapi import APIRouter, Depends

from app.domain.dto import HealthDto
from app.domain.result import Failure, Success
from app.infrastructure.di import health_usecase
from app.usecases.health import HealthUseCase

router = APIRouter(tags=["health"])


@router.get("/api/v1/health")
async def get_health(
    use_case: HealthUseCase = Depends(health_usecase),
) -> Success[HealthDto] | Failure:
    return await use_case()
