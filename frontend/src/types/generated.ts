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

export interface MeetingType {
  id: string;
  name: string;
  description: string;
  duration_minutes: number;
}

export interface CreateMeetingTypeRequest {
  name: string;
  description: string;
  duration_minutes: number;
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
