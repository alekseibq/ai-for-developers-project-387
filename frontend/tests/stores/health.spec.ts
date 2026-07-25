import { describe, it, expect, vi, beforeEach } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useHealthStore } from "@/stores/health";

const mockSuccess = {
  type: "success" as const,
  data: { status: "ok" as const, version: "0.1.0", database: "connected" as const, uptime: 42 },
};

const mockFailure = {
  type: "failure" as const,
  error: "Server error",
  code: "INTERNAL",
};

vi.mock("@/api/client", () => ({
  getHealth: vi.fn(),
}));

import { getHealth } from "@/api/client";
const mockedGetHealth = vi.mocked(getHealth);

describe("health store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("initialises with null health, null error, false loading", () => {
    const store = useHealthStore();

    expect(store.health).toBeNull();
    expect(store.error).toBeNull();
    expect(store.loading).toBe(false);
  });

  it("fetchHealth sets health on success", async () => {
    mockedGetHealth.mockResolvedValueOnce(mockSuccess);
    const store = useHealthStore();

    await store.fetchHealth();

    expect(store.health).toEqual(mockSuccess.data);
    expect(store.error).toBeNull();
    expect(store.loading).toBe(false);
  });

  it("fetchHealth sets error on API failure", async () => {
    mockedGetHealth.mockResolvedValueOnce(mockFailure);
    const store = useHealthStore();

    await store.fetchHealth();

    expect(store.error).toBe("Server error");
    expect(store.health).toBeNull();
    expect(store.loading).toBe(false);
  });

  it("fetchHealth sets 'Network error' on exception", async () => {
    mockedGetHealth.mockRejectedValueOnce(new Error("Network failure"));
    const store = useHealthStore();

    await store.fetchHealth();

    expect(store.error).toBe("Network error");
    expect(store.health).toBeNull();
    expect(store.loading).toBe(false);
  });

  it("startPolling calls fetchHealth immediately and sets interval", async () => {
    vi.useFakeTimers();
    mockedGetHealth.mockResolvedValue(mockSuccess);
    const store = useHealthStore();

    await store.startPolling(5000);

    expect(mockedGetHealth).toHaveBeenCalledTimes(1);

    vi.advanceTimersByTime(5000);
    expect(mockedGetHealth).toHaveBeenCalledTimes(2);

    vi.advanceTimersByTime(5000);
    expect(mockedGetHealth).toHaveBeenCalledTimes(3);

    vi.useRealTimers();
  });

  it("stopPolling clears interval", async () => {
    vi.useFakeTimers();
    mockedGetHealth.mockResolvedValue(mockSuccess);
    const store = useHealthStore();

    await store.startPolling(5000);
    expect(vi.getTimerCount()).toBe(1);

    store.stopPolling();
    expect(vi.getTimerCount()).toBe(0);

    vi.useRealTimers();
  });
});
