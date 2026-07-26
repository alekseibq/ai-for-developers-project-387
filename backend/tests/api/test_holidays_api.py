class TestGetHolidays:
    async def test_empty_list(self, test_client):
        response = await test_client.get("/api/v1/holidays")

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert body["data"] == []

    async def test_returns_created_holidays(self, test_client):
        await test_client.post(
            "/api/v1/holidays",
            json={
                "name": "New Year",
                "date": "2027-01-01",
            },
        )

        response = await test_client.get("/api/v1/holidays")

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert len(body["data"]) == 1
        assert body["data"][0]["name"] == "New Year"


class TestCreateHoliday:
    async def test_success(self, test_client):
        response = await test_client.post(
            "/api/v1/holidays",
            json={
                "name": "New Year",
                "date": "2027-01-01",
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"
        assert body["data"]["name"] == "New Year"
        assert body["data"]["date"] == "2027-01-01"
        assert "id" in body["data"]

    async def test_empty_name_fails(self, test_client):
        response = await test_client.post(
            "/api/v1/holidays",
            json={
                "name": "",
                "date": "2027-01-01",
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "failure"
        assert body["code"] == "INVALID_NAME"


class TestDeleteHoliday:
    async def test_success(self, test_client):
        create_resp = await test_client.post(
            "/api/v1/holidays",
            json={
                "name": "New Year",
                "date": "2027-01-01",
            },
        )
        holiday_id = create_resp.json()["data"]["id"]

        response = await test_client.delete(f"/api/v1/holidays/{holiday_id}")

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "success"

        get_resp = await test_client.get("/api/v1/holidays")
        assert len(get_resp.json()["data"]) == 0

    async def test_nonexistent_returns_failure(self, test_client):
        response = await test_client.delete("/api/v1/holidays/000000000000000000000000")

        assert response.status_code == 200
        body = response.json()
        assert body["type"] == "failure"
        assert body["code"] == "NOT_FOUND"
