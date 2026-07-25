from unittest.mock import AsyncMock

from app.domain.result import Failure
from app.infrastructure.di import list_all_meeting_type_usecase
from app.main import app


class TestGetMeetingTypes:
    async def test_empty_list(self, test_client):
        response = await test_client.get("/api/v1/meeting-types")

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert body["data"] == []

    async def test_returns_failure_when_usecase_fails(self, test_client):
        mock_usecase = AsyncMock()
        mock_usecase.return_value = Failure(error="DB error", code="DB_ERROR")

        app.dependency_overrides[list_all_meeting_type_usecase] = lambda: mock_usecase

        try:
            response = await test_client.get("/api/v1/meeting-types")

            assert response.status_code == 200
            body = response.json()
            assert body["type"] == "failure"
            assert body["code"] == "DB_ERROR"
        finally:
            app.dependency_overrides.clear()

    async def test_returns_created_types(self, test_client):
        await test_client.post(
            "/api/v1/meeting-types",
            json={
                "name": "Consultation",
                "description": "30 min meeting",
                "duration_minutes": 30,
            },
        )
        await test_client.post(
            "/api/v1/meeting-types",
            json={
                "name": "Workshop",
                "description": "60 min workshop",
                "duration_minutes": 60,
            },
        )

        response = await test_client.get("/api/v1/meeting-types")

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert len(body["data"]) == 2
        names = [t["name"] for t in body["data"]]
        assert "Consultation" in names
        assert "Workshop" in names


class TestCreateMeetingType:
    async def test_success(self, test_client):
        response = await test_client.post(
            "/api/v1/meeting-types",
            json={
                "name": "Consultation",
                "description": "30 min meeting",
                "duration_minutes": 30,
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert body["data"]["name"] == "Consultation"
        assert body["data"]["duration_minutes"] == 30
        assert "id" in body["data"]

    async def test_empty_name_fails(self, test_client):
        response = await test_client.post(
            "/api/v1/meeting-types",
            json={
                "name": "",
                "description": "desc",
                "duration_minutes": 30,
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "failure"
        assert body["code"] == "INVALID_NAME"

    async def test_zero_duration_fails(self, test_client):
        response = await test_client.post(
            "/api/v1/meeting-types",
            json={
                "name": "Test",
                "description": "desc",
                "duration_minutes": 0,
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "failure"
        assert body["code"] == "INVALID_DURATION"
