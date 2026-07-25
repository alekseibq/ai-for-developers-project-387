import { describe, it, expect, vi, afterEach } from "vitest";
import { getSlots } from "@/api/slots";

afterEach(() => {
  vi.unstubAllGlobals();
});

const mockSlots = [
  { start_time: "2026-06-15T09:00:00", end_time: "2026-06-15T09:30:00" },
  { start_time: "2026-06-15T09:30:00", end_time: "2026-06-15T10:00:00" },
];

const date = "2026-06-15";
const meetingTypeId = "abc123";

describe("getSlots", () => {
  it("calls GET /api/v1/slots with date and meeting_type_id", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ type: "success", data: [] }),
    });
    vi.stubGlobal("fetch", mockFetch);

    await getSlots(date, meetingTypeId);

    expect(mockFetch).toHaveBeenCalledOnce();
    expect(mockFetch).toHaveBeenCalledWith(
      `/api/v1/slots?date=${date}&meeting_type_id=${meetingTypeId}`
    );
  });

  it("encodes query parameters", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ type: "success", data: [] }),
    });
    vi.stubGlobal("fetch", mockFetch);

    await getSlots("2026-06-15", "abc 123");

    expect(mockFetch).toHaveBeenCalledWith(
      "/api/v1/slots?date=2026-06-15&meeting_type_id=abc%20123"
    );
  });

  it("returns slots on success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () => Promise.resolve({ type: "success", data: mockSlots }),
      })
    );

    const result = await getSlots(date, meetingTypeId);

    expect(result.type).toBe("success");
    if (result.type === "success") {
      expect(result.data).toEqual(mockSlots);
    }
  });

  it("returns error on failure", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () =>
          Promise.resolve({
            type: "failure",
            error: "Invalid date",
            code: "INVALID_DATE",
          }),
      })
    );

    const result = await getSlots(date, meetingTypeId);

    expect(result.type).toBe("failure");
    if (result.type === "failure") {
      expect(result.code).toBe("INVALID_DATE");
    }
  });
});
