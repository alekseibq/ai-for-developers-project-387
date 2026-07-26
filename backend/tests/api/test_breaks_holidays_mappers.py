from datetime import date, time

from app.api.v1.dto import BreakDto, HolidayDto
from app.api.v1.mappers import break_obj_to_dto, holiday_obj_to_dto
from app.domain.objects import BreakObj, HolidayObj


def test_break_obj_to_dto():
    obj = BreakObj(
        id="b1",
        name="Lunch",
        day_of_week=0,
        start_time=time(12, 0),
        end_time=time(13, 0),
    )

    dto = break_obj_to_dto(obj)

    assert isinstance(dto, BreakDto)
    assert dto.id == "b1"
    assert dto.name == "Lunch"
    assert dto.day_of_week == 0
    assert dto.start_time == time(12, 0)
    assert dto.end_time == time(13, 0)


def test_holiday_obj_to_dto():
    obj = HolidayObj(
        id="h1",
        name="New Year",
        date=date(2027, 1, 1),
    )

    dto = holiday_obj_to_dto(obj)

    assert isinstance(dto, HolidayDto)
    assert dto.id == "h1"
    assert dto.name == "New Year"
    assert dto.date == date(2027, 1, 1)
