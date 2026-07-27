export type HealthStatus = "ok" | "degraded";
export type DatabaseStatus = "connected" | "disconnected";

export interface HealthResponse {
  status: HealthStatus;
  version: string;
  database: DatabaseStatus;
  uptime: number;
}

export type Result<T> =
  | { type: "success"; data: T }
  | { type: "failure"; error: string; code: string };

export interface BreakDto {
  start_time: string;
  end_time: string;
}

export interface HolidayDto {
  date: string;
  name: string;
}

export interface MeetingType {
  id: string;
  name: string;
  description: string;
  duration_minutes: number;
  working_hours_start: string;
  working_hours_end: string;
  breaks: BreakDto[];
  holidays: HolidayDto[];
}

export interface CreateMeetingTypeRequest {
  name: string;
  description: string;
  duration_minutes: number;
}

export interface UpdateMeetingTypeRequest {
  name?: string;
  description?: string;
  duration_minutes?: number;
  working_hours_start?: string;
  working_hours_end?: string;
  breaks?: BreakDto[];
  holidays?: HolidayDto[];
}

export interface SlotDto {
  start_time: string;
  end_time: string;
}

export interface CreateBookingRequest {
  meeting_type_id: string;
  guest_name: string;
  start_time: string;
}

export interface BookingRichDto {
  id: string;
  guest_name: string;
  start_time: string;
  end_time: string;
  created_at: string;
  meeting_type: MeetingType;
}
