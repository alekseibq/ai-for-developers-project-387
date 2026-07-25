import { describe, it, expect, vi, beforeEach } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useBookingsStore } from "@/stores/bookings";

const mockSuccess = {
  type: "success" as const,
  data: [
    {
      id: "b1",
      guest_name: "John",
      start_time: "2026-06-15T14:00:00",
      end_time: "2026-06-15T15:00:00",
      created_at: "2026-06-13T12:00:00",
      meeting_type: {
        id: "mt1",
        name: "Consultation",
        description: "60 min",
        duration_minutes: 60,
      },
    },
  ],
};

const mockEmpty = { type: "success" as const, data: [] };

const mockFailure = {
  type: "failure" as const,
  error: "DB error",
  code: "DB_ERROR",
};

vi.mock("@/api/bookings", () => ({
  getBookings: vi.fn(),
  createBooking: vi.fn(),
}));

import { getBookings } from "@/api/bookings";
const mockedGet = vi.mocked(getBookings);

describe("bookings store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("initialises with empty array, null error, false loading", () => {
    const store = useBookingsStore();

    expect(store.bookings).toEqual([]);
    expect(store.error).toBeNull();
    expect(store.loading).toBe(false);
  });

  it("fetchBookings sets bookings on success", async () => {
    mockedGet.mockResolvedValueOnce(mockSuccess);
    const store = useBookingsStore();

    await store.fetchBookings();

    expect(store.bookings).toEqual(mockSuccess.data);
    expect(store.error).toBeNull();
    expect(store.loading).toBe(false);
  });

  it("fetchBookings sorts by start_time ascending", async () => {
    mockedGet.mockResolvedValueOnce({
      type: "success",
      data: [
        {
          id: "b2",
          guest_name: "Later",
          start_time: "2026-06-15T16:00:00",
          end_time: "2026-06-15T17:00:00",
          created_at: "2026-06-13T12:00:00",
          meeting_type: {
            id: "mt1",
            name: "Consultation",
            description: "60 min",
            duration_minutes: 60,
          },
        },
        {
          id: "b1",
          guest_name: "Earlier",
          start_time: "2026-06-15T14:00:00",
          end_time: "2026-06-15T15:00:00",
          created_at: "2026-06-13T12:00:00",
          meeting_type: {
            id: "mt1",
            name: "Consultation",
            description: "60 min",
            duration_minutes: 60,
          },
        },
      ],
    });
    const store = useBookingsStore();

    await store.fetchBookings();

    expect(store.bookings[0].guest_name).toBe("Earlier");
    expect(store.bookings[1].guest_name).toBe("Later");
  });

  it("fetchBookings sets empty array when data is empty", async () => {
    mockedGet.mockResolvedValueOnce(mockEmpty);
    const store = useBookingsStore();

    await store.fetchBookings();

    expect(store.bookings).toEqual([]);
    expect(store.loading).toBe(false);
  });

  it("fetchBookings sets error on API failure", async () => {
    mockedGet.mockResolvedValueOnce(mockFailure);
    const store = useBookingsStore();

    await store.fetchBookings();

    expect(store.error).toBe("DB error");
    expect(store.bookings).toEqual([]);
    expect(store.loading).toBe(false);
  });

  it("fetchBookings sets 'Network error' on exception", async () => {
    mockedGet.mockRejectedValueOnce(new Error("Network failure"));
    const store = useBookingsStore();

    await store.fetchBookings();

    expect(store.error).toBe("Network error");
    expect(store.loading).toBe(false);
  });
});
