model BreakDto {
  id: string;
  name: string;
  day_of_week: int32;
  start_time: string;
  end_time: string;
}

model CreateBreakRequest {
  name: string;
  day_of_week: int32;
  start_time: string;
  end_time: string;
}
