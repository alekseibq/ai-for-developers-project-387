import type { Result, BookingRichDto, CreateBookingRequest } from "@/types/generated";
import { post, request } from "./client";

export function createBooking(data: CreateBookingRequest): Promise<Result<BookingRichDto>> {
  return post<BookingRichDto>("/bookings", data);
}

export function getBookings(): Promise<Result<BookingRichDto[]>> {
  return request<BookingRichDto[]>("/bookings");
}
