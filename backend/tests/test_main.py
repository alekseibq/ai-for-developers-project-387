from unittest.mock import AsyncMock, patch

import pytest

from app.main import app, lifespan


@pytest.mark.asyncio
async def test_lifespan_connect_and_disconnect():
    mock_app = AsyncMock()

    with (
        patch("app.main.Database.connect") as mock_connect,
        patch("app.main.Database.disconnect") as mock_disconnect,
    ):
        async with lifespan(mock_app):
            mock_connect.assert_awaited_once()

        mock_disconnect.assert_awaited_once()


def test_app_routers_are_registered():
    routes = [route.path for route in app.routes]
    assert "/api/v1/health" in routes
    assert "/api/v1/meeting-types" in routes
    assert "/api/v1/slots" in routes
    assert "/api/v1/bookings" in routes
