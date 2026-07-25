import { describe, it, expect, vi, beforeEach } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useMeetingTypesStore } from "@/stores/meetingTypes";

const mockSuccess = {
  type: "success" as const,
  data: [
    { id: "1", name: "Consultation", description: "30 min", duration_minutes: 30 },
  ],
};

const mockEmpty = { type: "success" as const, data: [] };

const mockFailure = {
  type: "failure" as const,
  error: "DB error",
  code: "DB_ERROR",
};

const mockCreateSuccess = {
  type: "success" as const,
  data: { id: "3", name: "New", description: "Desc", duration_minutes: 45 },
};

const mockCreateFailure = {
  type: "failure" as const,
  error: "Name is required",
  code: "INVALID_NAME",
};

vi.mock("@/api/meetingTypes", () => ({
  getMeetingTypes: vi.fn(),
  createMeetingType: vi.fn(),
}));

import { getMeetingTypes, createMeetingType } from "@/api/meetingTypes";
const mockedGet = vi.mocked(getMeetingTypes);
const mockedCreate = vi.mocked(createMeetingType);

describe("meetingTypes store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("initialises with empty array, null error, false loading", () => {
    const store = useMeetingTypesStore();

    expect(store.meetingTypes).toEqual([]);
    expect(store.error).toBeNull();
    expect(store.loading).toBe(false);
  });

  it("fetchMeetingTypes sets meetingTypes on success", async () => {
    mockedGet.mockResolvedValueOnce(mockSuccess);
    const store = useMeetingTypesStore();

    await store.fetchMeetingTypes();

    expect(store.meetingTypes).toEqual(mockSuccess.data);
    expect(store.error).toBeNull();
    expect(store.loading).toBe(false);
  });

  it("fetchMeetingTypes sets empty array when data is empty", async () => {
    mockedGet.mockResolvedValueOnce(mockEmpty);
    const store = useMeetingTypesStore();

    await store.fetchMeetingTypes();

    expect(store.meetingTypes).toEqual([]);
    expect(store.loading).toBe(false);
  });

  it("fetchMeetingTypes sets error on API failure", async () => {
    mockedGet.mockResolvedValueOnce(mockFailure);
    const store = useMeetingTypesStore();

    await store.fetchMeetingTypes();

    expect(store.error).toBe("DB error");
    expect(store.meetingTypes).toEqual([]);
    expect(store.loading).toBe(false);
  });

  it("fetchMeetingTypes sets 'Network error' on exception", async () => {
    mockedGet.mockRejectedValueOnce(new Error("Network failure"));
    const store = useMeetingTypesStore();

    await store.fetchMeetingTypes();

    expect(store.error).toBe("Network error");
    expect(store.loading).toBe(false);
  });

  it("create returns success result", async () => {
    mockedCreate.mockResolvedValueOnce(mockCreateSuccess);
    const store = useMeetingTypesStore();

    const result = await store.create({
      name: "New",
      description: "Desc",
      duration_minutes: 45,
    });

    expect(result.type).toBe("success");
    if (result.type === "success") {
      expect(result.data).toEqual(mockCreateSuccess.data);
    }
  });

  it("create returns failure result on API error", async () => {
    mockedCreate.mockResolvedValueOnce(mockCreateFailure);
    const store = useMeetingTypesStore();

    const result = await store.create({
      name: "",
      description: "Desc",
      duration_minutes: 45,
    });

    expect(result.type).toBe("failure");
    if (result.type === "failure") {
      expect(result.code).toBe("INVALID_NAME");
    }
  });

  it("create returns failure result on network error", async () => {
    mockedCreate.mockRejectedValueOnce(new Error("Network failure"));
    const store = useMeetingTypesStore();

    const result = await store.create({
      name: "Test",
      description: "Desc",
      duration_minutes: 30,
    });

    expect(result.type).toBe("failure");
    if (result.type === "failure") {
      expect(result.code).toBe("NETWORK");
      expect(result.error).toBe("Network error");
    }
  });
});
