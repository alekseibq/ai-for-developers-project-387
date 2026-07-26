model HolidayDto {
  id: string;
  name: string;
  date: string;
}

model CreateHolidayRequest {
  name: string;
  date: string;
}
