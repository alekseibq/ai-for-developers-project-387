from datetime import date

from app.domain.objects import SlotObj
from app.domain.result import Failure, Success
from app.repositories.meeting_type_repository import MeetingTypeRepository
from app.services.propose_slot_dates_service import ProposeSlotDatesService
from app.services.slot_service import SlotService


class FindSlotsUseCase:
    def __init__(
        self,
        slot_service: SlotService,
        propose_dates_service: ProposeSlotDatesService,
        meeting_type_repo: MeetingTypeRepository,
    ):
        self._slot_service = slot_service
        self._propose_dates_service = propose_dates_service
        self._meeting_type_repo = meeting_type_repo

    async def __call__(
        self, date_str: str, meeting_type_id: str
    ) -> Success[list[SlotObj]] | Failure:
        try:
            day = date.fromisoformat(date_str)
        except ValueError:
            return Failure(error="Invalid date format, expected YYYY-MM-DD", code="INVALID_DATE")

        date_range = await self._propose_dates_service()
        if day < date_range.min_date or day > date_range.max_date:
            return Failure(error="Date is outside booking window", code="OUTSIDE_BOOKING_WINDOW")

        meeting_type = await self._meeting_type_repo.find_by_id(meeting_type_id)
        if not meeting_type:
            return Failure(error="Meeting type not found", code="MEETING_TYPE_NOT_FOUND")

        slots = await self._slot_service.find_available_slots(day, meeting_type)
        return Success(data=slots)
