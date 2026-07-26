import type { Result, HolidayDto, CreateHolidayRequest } from "@/types/generated";
import { request, post, del } from "./client";

export function getHolidays(): Promise<Result<HolidayDto[]>> {
  return request<HolidayDto[]>("/holidays");
}

export function createHoliday(data: CreateHolidayRequest): Promise<Result<HolidayDto>> {
  return post<HolidayDto>("/holidays", data);
}

export function deleteHoliday(id: string): Promise<Result<null>> {
  return del<null>(`/holidays/${encodeURIComponent(id)}`);
}
