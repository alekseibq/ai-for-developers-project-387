import type { Result, BreakDto, CreateBreakRequest } from "@/types/generated";
import { request, post, del } from "./client";

export function getBreaks(): Promise<Result<BreakDto[]>> {
  return request<BreakDto[]>("/breaks");
}

export function createBreak(data: CreateBreakRequest): Promise<Result<BreakDto>> {
  return post<BreakDto>("/breaks", data);
}

export function deleteBreak(id: string): Promise<Result<null>> {
  return del<null>(`/breaks/${encodeURIComponent(id)}`);
}
