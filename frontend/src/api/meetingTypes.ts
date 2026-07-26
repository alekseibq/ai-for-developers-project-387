import type { Result, MeetingType, CreateMeetingTypeRequest, UpdateMeetingTypeRequest } from "@/types/generated";
import { request, post, patch } from "./client";

export function getMeetingTypes(): Promise<Result<MeetingType[]>> {
  return request<MeetingType[]>("/meeting-types");
}

export function getMeetingType(id: string): Promise<Result<MeetingType>> {
  return request<MeetingType>(`/meeting-types/${id}`);
}

export function createMeetingType(
  data: CreateMeetingTypeRequest
): Promise<Result<MeetingType>> {
  return post<MeetingType>("/meeting-types", data);
}

export function updateMeetingType(
  id: string,
  data: UpdateMeetingTypeRequest
): Promise<Result<MeetingType>> {
  return patch<MeetingType>(`/meeting-types/${id}`, data);
}
