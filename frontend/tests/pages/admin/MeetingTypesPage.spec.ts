import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { useMeetingTypesStore } from "@/stores/meetingTypes";
import MeetingTypesPage from "@/pages/admin/MeetingTypesPage.vue";

vi.mock("@/api/meetingTypes", () => ({
  getMeetingTypes: vi.fn(),
  createMeetingType: vi.fn(),
}));

import { getMeetingTypes } from "@/api/meetingTypes";
import type { Mock } from "vitest";

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: "/admin",
      component: { template: "<div><router-view /></div>" },
      children: [
        { path: "meeting_types", component: MeetingTypesPage },
        { path: "meeting_types/new", component: { template: "<div>New</div>" } },
      ],
    },
  ],
});

function mountPage() {
  const pinia = createPinia();
  const wrapper = mount(MeetingTypesPage, {
    global: { plugins: [router, pinia] },
  });
  const store = useMeetingTypesStore(pinia);
  return { wrapper, store, pinia };
}

describe("MeetingTypesPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getMeetingTypes as Mock).mockResolvedValue({ type: "success", data: [] });
  });

  it("shows loading state", async () => {
    (getMeetingTypes as Mock).mockImplementation(
      () => new Promise(() => {})
    );

    await router.push("/admin/meeting_types");
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

    await router.push("/admin/meeting_types");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("Failed to load");
  });

  it("shows empty message when no meeting types", async () => {
    (getMeetingTypes as Mock).mockResolvedValue({ type: "success", data: [] });

    await router.push("/admin/meeting_types");
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

    await router.push("/admin/meeting_types");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("Consultation");
    expect(wrapper.text()).toContain("abc123");
    expect(wrapper.text()).toContain("30 min meeting");
    expect(wrapper.text()).toContain("30 мин");
  });

  it("renders multiple meeting types", async () => {
    (getMeetingTypes as Mock).mockResolvedValue({
      type: "success",
      data: [
        { id: "1", name: "Type A", description: "Desc A", duration_minutes: 15 },
        { id: "2", name: "Type B", description: "Desc B", duration_minutes: 60 },
      ],
    });

    await router.push("/admin/meeting_types");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("Type A");
    expect(wrapper.text()).toContain("Type B");
    expect(wrapper.text()).toContain("15 мин");
    expect(wrapper.text()).toContain("60 мин");
  });

  it("navigates to create page on button click", async () => {
    await router.push("/admin/meeting_types");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);

    const push = vi.spyOn(router, "push");
    await wrapper.find("button").trigger("click");

    expect(push).toHaveBeenCalledWith("/admin/meeting_types/new");
  });
});
