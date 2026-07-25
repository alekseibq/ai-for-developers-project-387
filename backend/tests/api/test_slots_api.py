from datetime import date, timedelta

TODAY = date.today()


class TestGetSlots:
    async def test_success(self, test_client):
        mt_resp = await test_client.post(
            "/api/v1/meeting-types",
            json={
                "name": "Consultation",
                "description": "30 min",
                "duration_minutes": 30,
            },
        )
        mt_id = mt_resp.json()["data"]["id"]

        monday = _next_weekday(TODAY)
        response = await test_client.get(
            f"/api/v1/slots?date={monday.isoformat()}&meeting_type_id={mt_id}",
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert len(body["data"]) == 18
        assert body["data"][0]["start_time"] is not None

    async def test_invalid_date_format_fails(self, test_client):
        mt_resp = await test_client.post(
            "/api/v1/meeting-types",
            json={
                "name": "Consultation",
                "description": "30 min",
                "duration_minutes": 30,
            },
        )
        mt_id = mt_resp.json()["data"]["id"]

        response = await test_client.get(
            f"/api/v1/slots?date=not-a-date&meeting_type_id={mt_id}",
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "failure"
        assert body["code"] == "INVALID_DATE"

    async def test_weekend_returns_empty(self, test_client):
        mt_resp = await test_client.post(
            "/api/v1/meeting-types",
            json={
                "name": "Consultation",
                "description": "30 min",
                "duration_minutes": 30,
            },
        )
        mt_id = mt_resp.json()["data"]["id"]

        saturday = _next_saturday(TODAY)
        response = await test_client.get(
            f"/api/v1/slots?date={saturday.isoformat()}&meeting_type_id={mt_id}",
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert body["data"] == []

    async def test_nonexistent_meeting_type_fails(self, test_client):
        fake_id = "000000000000000000000000"

        monday = _next_weekday(TODAY)
        response = await test_client.get(
            f"/api/v1/slots?date={monday.isoformat()}&meeting_type_id={fake_id}",
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "failure"
        assert body["code"] == "MEETING_TYPE_NOT_FOUND"


def _next_weekday(d: date) -> date:
    for i in range(7):
        candidate = d + timedelta(days=i)
        if candidate.weekday() < 5:
            return candidate
    return d


def _next_saturday(d: date) -> date:
    for i in range(7):
        candidate = d + timedelta(days=i)
        if candidate.weekday() == 5:
            return candidate
    return d
