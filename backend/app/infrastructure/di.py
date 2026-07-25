from fastapi import Depends

from app.repositories.booking_repository import BookingRepository
from app.repositories.health import HealthRepository
from app.repositories.meeting_type_repository import MeetingTypeRepository
from app.services.propose_slot_dates_service import ProposeSlotDatesService
from app.services.slot_service import SlotService
from app.usecases.create_booking_use_case import CreateBookingUseCase
from app.usecases.create_meeting_type_use_case import CreateMeetingTypeUseCase
from app.usecases.find_slots_use_case import FindSlotsUseCase
from app.usecases.health import HealthUseCase
from app.usecases.list_all_meeting_type_use_case import ListAllMeetingTypeUseCase
from app.usecases.list_upcoming_bookings_use_case import ListUpcomingBookingsUseCase


def health_repository() -> HealthRepository:
    return HealthRepository()


def health_usecase(
    repo: HealthRepository = Depends(health_repository),
) -> HealthUseCase:
    return HealthUseCase(repo=repo)


def meeting_type_repository() -> MeetingTypeRepository:
    return MeetingTypeRepository()


def booking_repository() -> BookingRepository:
    return BookingRepository()


def slot_service(
    booking_repo: BookingRepository = Depends(booking_repository),
) -> SlotService:
    return SlotService(booking_repo=booking_repo)


def propose_slot_dates_service() -> ProposeSlotDatesService:
    return ProposeSlotDatesService()


def list_all_meeting_type_usecase(
    repo: MeetingTypeRepository = Depends(meeting_type_repository),
) -> ListAllMeetingTypeUseCase:
    return ListAllMeetingTypeUseCase(repo=repo)


def create_meeting_type_usecase(
    repo: MeetingTypeRepository = Depends(meeting_type_repository),
) -> CreateMeetingTypeUseCase:
    return CreateMeetingTypeUseCase(repo=repo)


def find_slots_usecase(
    slot_service: SlotService = Depends(slot_service),
    propose_dates_service: ProposeSlotDatesService = Depends(propose_slot_dates_service),
    meeting_type_repo: MeetingTypeRepository = Depends(meeting_type_repository),
) -> FindSlotsUseCase:
    return FindSlotsUseCase(
        slot_service=slot_service,
        propose_dates_service=propose_dates_service,
        meeting_type_repo=meeting_type_repo,
    )


def create_booking_usecase(
    booking_repo: BookingRepository = Depends(booking_repository),
    meeting_type_repo: MeetingTypeRepository = Depends(meeting_type_repository),
) -> CreateBookingUseCase:
    return CreateBookingUseCase(
        booking_repo=booking_repo,
        meeting_type_repo=meeting_type_repo,
    )


def list_upcoming_bookings_usecase(
    booking_repo: BookingRepository = Depends(booking_repository),
) -> ListUpcomingBookingsUseCase:
    return ListUpcomingBookingsUseCase(booking_repo=booking_repo)
