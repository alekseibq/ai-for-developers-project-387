from datetime import datetime, timedelta

import pytest

from app.services.propose_slot_dates_service import ProposeSlotDatesService


@pytest.mark.asyncio
async def test_returns_today_and_today_plus_13_days():
    service = ProposeSlotDatesService()

    result = await service()

    today = datetime.utcnow().date()
    assert result.min_date == today
    assert result.max_date == today + timedelta(days=13)
