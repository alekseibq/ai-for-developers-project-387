import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { setActivePinia, createPinia } from "pinia";
import { useHealthStore } from "@/stores/health";
import HealthIndicator from "@/components/HealthIndicator.vue";

vi.mock("@/api/client", () => ({
  getHealth: vi.fn(),
}));

describe("HealthIndicator", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("renders without crashing", () => {
    const wrapper = mount(HealthIndicator);
    expect(wrapper.exists()).toBe(true);
  });

  it("shows 'checking...' when loading", () => {
    const store = useHealthStore();
    store.loading = true;
    const wrapper = mount(HealthIndicator);

    expect(wrapper.text()).toContain("checking...");
  });

  it("shows green dot and status text when healthy", () => {
    const store = useHealthStore();
    store.health = { status: "ok", version: "0.1.0", database: "connected", uptime: 42 };
    const wrapper = mount(HealthIndicator);

    expect(wrapper.find(".bg-green-500").exists()).toBe(true);
    expect(wrapper.text()).toContain("ok · v0.1.0");
  });

  it("shows yellow dot and degraded text when degraded", () => {
    const store = useHealthStore();
    store.health = { status: "degraded", version: "0.1.0", database: "disconnected", uptime: 42 };
    const wrapper = mount(HealthIndicator);

    expect(wrapper.find(".bg-yellow-500").exists()).toBe(true);
    expect(wrapper.text()).toContain("degraded · v0.1.0");
  });

  it("shows 'offline' when error is set", () => {
    const store = useHealthStore();
    store.error = "Network error";
    const wrapper = mount(HealthIndicator);

    expect(wrapper.find(".bg-red-500").exists()).toBe(true);
    expect(wrapper.text()).toContain("offline");
  });

  it("calls startPolling on mount", () => {
    const store = useHealthStore();
    const spy = vi.spyOn(store, "startPolling");
    mount(HealthIndicator);

    expect(spy).toHaveBeenCalledOnce();
  });
});
