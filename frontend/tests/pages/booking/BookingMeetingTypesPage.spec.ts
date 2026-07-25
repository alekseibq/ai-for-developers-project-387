import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { useMeetingTypesStore } from "@/stores/meetingTypes";
import BookingMeetingTypesPage from "@/pages/booking/BookingMeetingTypesPage.vue";

vi.mock("@/api/meetingTypes", () => ({
  getMeetingTypes: vi.fn(),
  createMeetingType: vi.fn(),
}));

import { getMeetingTypes } from "@/api/meetingTypes";
import type { Mock } from "vitest";

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    { path: "/booking", component: BookingMeetingTypesPage },
    { path: "/booking/:meetingTypeId", component: { template: "<div>Slot page</div>" } },
  ],
});

function mountPage() {
  const pinia = createPinia();
  const wrapper = mount(BookingMeetingTypesPage, {
    global: { plugins: [router, pinia] },
  });
  const store = useMeetingTypesStore(pinia);
  return { wrapper, store, pinia };
}

describe("BookingMeetingTypesPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getMeetingTypes as Mock).mockResolvedValue({ type: "success", data: [] });
  });

  it("shows loading state", async () => {
    (getMeetingTypes as Mock).mockImplementation(
      () => new Promise(() => {})
    );

    await router.push("/booking");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain("Загрузка...");
  });

  it("shows error message when error is set", async () => {
    (getMeetingTypes as Mock).mockResolvedValue({
      type: "failure",
      error: "Failed to load",
      code: "DB_ERROR",
    });

    await router.push("/booking");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("Failed to load");
  });

  it("shows empty message when no meeting types", async () => {
    await router.push("/booking");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("Пока нет ни одного типа события");
  });

  it("renders list of meeting types", async () => {
    (getMeetingTypes as Mock).mockResolvedValue({
      type: "success",
      data: [
        { id: "abc123", name: "Consultation", description: "30 min meeting", duration_minutes: 30 },
      ],
    });

    await router.push("/booking");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("Consultation");
    expect(wrapper.text()).toContain("30 min meeting");
    expect(wrapper.text()).toContain("30 мин");
  });

  it("does not show meeting type ID in card", async () => {
    (getMeetingTypes as Mock).mockResolvedValue({
      type: "success",
      data: [
        { id: "abc123", name: "Consultation", description: "30 min meeting", duration_minutes: 30 },
      ],
    });

    await router.push("/booking");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).not.toContain("abc123");
  });

  it("renders multiple meeting types", async () => {
    (getMeetingTypes as Mock).mockResolvedValue({
      type: "success",
      data: [
        { id: "1", name: "Type A", description: "Desc A", duration_minutes: 15 },
        { id: "2", name: "Type B", description: "Desc B", duration_minutes: 60 },
      ],
    });

    await router.push("/booking");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("Type A");
    expect(wrapper.text()).toContain("Type B");
    expect(wrapper.text()).toContain("15 мин");
    expect(wrapper.text()).toContain("60 мин");
  });

  it("navigates to slot page on card click", async () => {
    (getMeetingTypes as Mock).mockResolvedValue({
      type: "success",
      data: [
        { id: "abc123", name: "Consultation", description: "30 min meeting", duration_minutes: 30 },
      ],
    });

    await router.push("/booking");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);

    const push = vi.spyOn(router, "push");
    const card = wrapper.find('[role="button"]');
    await card.trigger("click");

    expect(push).toHaveBeenCalledWith("/booking/abc123");
  });
});
