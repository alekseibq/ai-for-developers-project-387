model BreakDto {
  start_time: string;
  end_time: string;
}

model HolidayDto {
  date: plainDate;
  name: string;
}

model MeetingTypeDto {
  id: string;
  name: string;
  description: string;
  duration_minutes: int32;
  working_hours_start: string;
  working_hours_end: string;
  breaks: BreakDto[];
  holidays: HolidayDto[];
}

model CreateMeetingTypeRequest {
  name: string;
  description: string;
  duration_minutes: int32;
}

model UpdateMeetingTypeRequest {
  name?: string;
  description?: string;
  duration_minutes?: int32;
  working_hours_start?: string;
  working_hours_end?: string;
  breaks?: BreakDto[];
  holidays?: HolidayDto[];
}
