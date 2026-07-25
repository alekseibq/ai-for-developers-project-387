model MeetingTypeDto {
  id: string;
  name: string;
  description: string;
  duration_minutes: int32;
}

model CreateMeetingTypeRequest {
  name: string;
  description: string;
  duration_minutes: int32;
}
