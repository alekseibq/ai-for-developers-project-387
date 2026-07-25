import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import CreateMeetingTypePage from "@/pages/admin/CreateMeetingTypePage.vue";

const toastMock = vi.hoisted(() => ({
  success: vi.fn(),
  error: vi.fn(),
}));

vi.mock("@/api/meetingTypes", () => ({
  getMeetingTypes: vi.fn(),
  createMeetingType: vi.fn(),
}));

vi.mock("vue-toastification", () => ({
  useToast: () => toastMock,
}));

import { createMeetingType } from "@/api/meetingTypes";
import type { Mock } from "vitest";

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: "/admin",
      component: { template: "<div><router-view /></div>" },
      children: [
        { path: "meeting_types", component: { template: "<div>List</div>" } },
        { path: "meeting_types/new", component: CreateMeetingTypePage },
      ],
    },
  ],
});

function mountPage() {
  const pinia = createPinia();
  const wrapper = mount(CreateMeetingTypePage, {
    global: { plugins: [router, pinia] },
  });
  return { wrapper, pinia };
}

async function fillForm(wrapper: ReturnType<typeof mount>) {
  const inputs = wrapper.findAll("input");
  await inputs[0].setValue("Test");
  const textarea = wrapper.find("textarea");
  await textarea.setValue("Desc");
  await inputs[1].setValue(30);
}

describe("CreateMeetingTypePage", () => {
  beforeEach(async () => {
    vi.clearAllMocks();
    (createMeetingType as Mock).mockResolvedValue({
      type: "success",
      data: { id: "1", name: "Test", description: "Desc", duration_minutes: 30 },
    });
    await router.push("/admin/meeting_types/new");
    await router.isReady();
  });

  it("renders form with all fields and buttons", async () => {
    const { wrapper } = mountPage();

    expect(wrapper.find("input[type='text']").exists()).toBe(true);
    expect(wrapper.find("textarea").exists()).toBe(true);
    expect(wrapper.find("input[type='number']").exists()).toBe(true);
    expect(wrapper.text()).toContain("Отменить");
    expect(wrapper.text()).toContain("Создать");
  });

  it("cancel button navigates back to meeting types list", async () => {
    const { wrapper } = mountPage();
    const push = vi.spyOn(router, "push");

    await wrapper.findAll("button")[0].trigger("click");

    expect(push).toHaveBeenCalledWith("/admin/meeting_types");
  });

  it("shows validation errors when submitting empty form", async () => {
    const { wrapper } = mountPage();

    await wrapper.find("form").trigger("submit");

    expect(wrapper.text()).toContain("Название обязательно");
    expect(wrapper.text()).toContain("Описание обязательно");
    expect(wrapper.text()).toContain("Длительность должна быть не менее 1 минуты");
  });

  it("shows validation error for duration less than 1", async () => {
    const { wrapper } = mountPage();
    const inputs = wrapper.findAll("input");
    await inputs[0].setValue("Test");
    const textarea = wrapper.find("textarea");
    await textarea.setValue("Desc");
    await inputs[1].setValue(0);

    await wrapper.find("form").trigger("submit");

    expect(wrapper.text()).toContain("Длительность должна быть не менее 1 минуты");
  });

  it("calls createMeetingType and shows success toast on valid submit", async () => {
    const { wrapper } = mountPage();
    const push = vi.spyOn(router, "push");

    await fillForm(wrapper);
    await wrapper.find("form").trigger("submit");
    await new Promise(process.nextTick);

    expect(createMeetingType).toHaveBeenCalledWith({
      name: "Test",
      description: "Desc",
      duration_minutes: 30,
    });
    expect(toastMock.success).toHaveBeenCalledWith("Тип события успешно создан");
    expect(push).toHaveBeenCalledWith("/admin/meeting_types");
  });

  it("shows error toast for INVALID_NAME backend error", async () => {
    (createMeetingType as Mock).mockResolvedValue({
      type: "failure",
      error: "Name is required",
      code: "INVALID_NAME",
    });

    const { wrapper } = mountPage();
    await fillForm(wrapper);
    await wrapper.find("form").trigger("submit");
    await new Promise(process.nextTick);

    expect(toastMock.error).toHaveBeenCalledWith("Название не может быть пустым", {
      timeout: 8000,
    });
  });

  it("shows error toast for network error", async () => {
    (createMeetingType as Mock).mockRejectedValue(new Error("Network failure"));

    const { wrapper } = mountPage();
    await fillForm(wrapper);
    await wrapper.find("form").trigger("submit");
    await new Promise(process.nextTick);

    expect(toastMock.error).toHaveBeenCalledWith("Сервер недоступен. Попробуйте позже.", {
      timeout: 8000,
    });
  });

  it("shows generic error toast for unknown backend error code", async () => {
    (createMeetingType as Mock).mockResolvedValue({
      type: "failure",
      error: "Something went wrong",
      code: "UNKNOWN_ERROR",
    });

    const { wrapper } = mountPage();
    await fillForm(wrapper);
    await wrapper.find("form").trigger("submit");
    await new Promise(process.nextTick);

    expect(toastMock.error).toHaveBeenCalledWith("Something went wrong", {
      timeout: 8000,
    });
  });
});
