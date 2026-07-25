model BookingRawDto {
  id: string;
  meeting_type_id: string;
  guest_name: string;
  start_time: utcDateTime;
  created_at: utcDateTime;
}

model BookingRichDto {
  id: string;
  guest_name: string;
  start_time: utcDateTime;
  end_time: utcDateTime;
  created_at: utcDateTime;
  meeting_type: MeetingTypeDto;
}

model CreateBookingRequest {
  meeting_type_id: string;
  guest_name: string;
  start_time: utcDateTime;
}
