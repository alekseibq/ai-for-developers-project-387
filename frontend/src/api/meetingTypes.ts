import type { Result, MeetingType, CreateMeetingTypeRequest } from "@/types/generated";
import { request, post } from "./client";

export function getMeetingTypes(): Promise<Result<MeetingType[]>> {
  return request<MeetingType[]>("/meeting-types");
}

export function createMeetingType(
  data: CreateMeetingTypeRequest
): Promise<Result<MeetingType>> {
  return post<MeetingType>("/meeting-types", data);
}
