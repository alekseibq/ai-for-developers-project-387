import type { Result, SlotDto } from "@/types/generated";
import { request } from "./client";

export function getSlots(
  date: string,
  meetingTypeId: string
): Promise<Result<SlotDto[]>> {
  return request<SlotDto[]>(
    `/slots?date=${encodeURIComponent(date)}&meeting_type_id=${encodeURIComponent(meetingTypeId)}`
  );
}
