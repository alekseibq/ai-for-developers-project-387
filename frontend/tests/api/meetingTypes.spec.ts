import { describe, it, expect, vi, afterEach } from "vitest";
import { getMeetingTypes, createMeetingType } from "@/api/meetingTypes";

afterEach(() => {
  vi.unstubAllGlobals();
});

const mockMeetingTypes = [
  { id: "1", name: "Consultation", description: "30 min", duration_minutes: 30 },
  { id: "2", name: "Workshop", description: "60 min", duration_minutes: 60 },
];

describe("getMeetingTypes", () => {
  it("calls GET /api/v1/meeting-types", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ type: "success", data: [] }),
    });
    vi.stubGlobal("fetch", mockFetch);

    await getMeetingTypes();

    expect(mockFetch).toHaveBeenCalledOnce();
    expect(mockFetch).toHaveBeenCalledWith("/api/v1/meeting-types");
  });

  it("returns meeting types on success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () => Promise.resolve({ type: "success", data: mockMeetingTypes }),
      })
    );

    const result = await getMeetingTypes();

    expect(result.type).toBe("success");
    if (result.type === "success") {
      expect(result.data).toEqual(mockMeetingTypes);
    }
  });

  it("returns error on failure", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () =>
          Promise.resolve({ type: "failure", error: "DB error", code: "DB_ERROR" }),
      })
    );

    const result = await getMeetingTypes();

    expect(result.type).toBe("failure");
    if (result.type === "failure") {
      expect(result.error).toBe("DB error");
    }
  });
});

describe("createMeetingType", () => {
  const payload = { name: "Test", description: "Desc", duration_minutes: 30 };

  it("calls POST /api/v1/meeting-types with the request body", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ type: "success", data: { id: "3", ...payload } }),
    });
    vi.stubGlobal("fetch", mockFetch);

    await createMeetingType(payload);

    expect(mockFetch).toHaveBeenCalledOnce();
    expect(mockFetch).toHaveBeenCalledWith("/api/v1/meeting-types", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  });

  it("returns created meeting type on success", async () => {
    const created = { id: "3", ...payload };
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () => Promise.resolve({ type: "success", data: created }),
      })
    );

    const result = await createMeetingType(payload);

    expect(result.type).toBe("success");
    if (result.type === "success") {
      expect(result.data).toEqual(created);
    }
  });

  it("returns error on failure", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        json: () =>
          Promise.resolve({
            type: "failure",
            error: "Name is required",
            code: "INVALID_NAME",
          }),
      })
    );

    const result = await createMeetingType(payload);

    expect(result.type).toBe("failure");
    if (result.type === "failure") {
      expect(result.code).toBe("INVALID_NAME");
    }
  });
});
