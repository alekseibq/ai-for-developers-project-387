import { describe, it, expect, vi, afterEach } from "vitest";
import { getHealth, post } from "@/api/client";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("getHealth", () => {
  it("calls fetch with /api/v1/health", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ type: "success", data: null }),
    });
    vi.stubGlobal("fetch", mockFetch);

    await getHealth();

    expect(mockFetch).toHaveBeenCalledOnce();
    expect(mockFetch).toHaveBeenCalledWith("/api/v1/health");
  });

  it("returns data on success response", async () => {
    const healthData = {
      status: "ok",
      version: "0.1.0",
      database: "connected",
      uptime: 42,
    };
    const mockFetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ type: "success", data: healthData }),
    });
    vi.stubGlobal("fetch", mockFetch);

    const result = await getHealth();

    expect(result.type).toBe("success");
    if (result.type === "success") {
      expect(result.data).toEqual(healthData);
    }
  });

  it("returns error on failure response", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: () =>
        Promise.resolve({ type: "failure", error: "Server error", code: "INTERNAL" }),
    });
    vi.stubGlobal("fetch", mockFetch);

    const result = await getHealth();

    expect(result.type).toBe("failure");
    if (result.type === "failure") {
      expect(result.error).toBe("Server error");
      expect(result.code).toBe("INTERNAL");
    }
  });

  it("propagates network error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("Network failure")));

    await expect(getHealth()).rejects.toThrow("Network failure");
  });
});

describe("post", () => {
  it("sends POST with JSON body to the correct URL", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ type: "success", data: null }),
    });
    vi.stubGlobal("fetch", mockFetch);

    await post("/test", { foo: "bar" });

    expect(mockFetch).toHaveBeenCalledOnce();
    expect(mockFetch).toHaveBeenCalledWith("/api/v1/test", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ foo: "bar" }),
    });
  });

  it("returns data on success response", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ type: "success", data: { id: "1" } }),
    });
    vi.stubGlobal("fetch", mockFetch);

    const result = await post("/test", {});

    expect(result.type).toBe("success");
    if (result.type === "success") {
      expect(result.data).toEqual({ id: "1" });
    }
  });

  it("returns error on failure response", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: () =>
        Promise.resolve({ type: "failure", error: "Bad request", code: "BAD_REQUEST" }),
    });
    vi.stubGlobal("fetch", mockFetch);

    const result = await post("/test", {});

    expect(result.type).toBe("failure");
    if (result.type === "failure") {
      expect(result.error).toBe("Bad request");
      expect(result.code).toBe("BAD_REQUEST");
    }
  });

  it("propagates network error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("Network failure")));

    await expect(post("/test", {})).rejects.toThrow("Network failure");
  });
});
