import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { useMeetingTypesStore } from "@/stores/meetingTypes";
import BookingSlotPage from "@/pages/booking/BookingSlotPage.vue";

vi.mock("@/api/meetingTypes", () => ({
  getMeetingTypes: vi.fn(),
  createMeetingType: vi.fn(),
}));

vi.mock("@/api/slots", () => ({
  getSlots: vi.fn(),
}));

vi.mock("@/api/bookings", () => ({
  createBooking: vi.fn(),
}));

import { getSlots } from "@/api/slots";
import { createBooking } from "@/api/bookings";
import type { Mock } from "vitest";

const meetingType = {
  id: "mt-1",
  name: "Consultation",
  description: "30 min meeting",
  duration_minutes: 30,
};

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    { path: "/booking", component: { template: "<div>Booking list</div>" } },
    {
      path: "/booking/:meetingTypeId",
      component: BookingSlotPage,
    },
  ],
});

function mountPage() {
  const pinia = createPinia();
  setActivePinia(pinia);
  const store = useMeetingTypesStore(pinia);
  // Pre-populate store so onMounted doesn't fetch
  store.meetingTypes = [meetingType];
  store.loading = false;
  store.error = null;

  const wrapper = mount(BookingSlotPage, {
    global: { plugins: [router, pinia] },
  });
  return { wrapper, store, pinia };
}

const mockSlots = [
  { start_time: "2026-06-15T09:00:00", end_time: "2026-06-15T09:30:00" },
  { start_time: "2026-06-15T10:00:00", end_time: "2026-06-15T10:30:00" },
];

const mockBookingResult = {
  id: "b-1",
  guest_name: "John",
  start_time: "2026-06-15T09:00:00",
  end_time: "2026-06-15T09:30:00",
  created_at: "2026-06-13T12:00:00",
  meeting_type: meetingType,
};

describe("BookingSlotPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-06-13"));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("shows loading when store is loading", async () => {
    const pinia = createPinia();
    setActivePinia(pinia);
    const store = useMeetingTypesStore(pinia);
    store.meetingTypes = [];
    store.loading = true;

    await router.push("/booking/mt-1");
    await router.isReady();

    const wrapper = mount(BookingSlotPage, {
      global: { plugins: [router, pinia] },
    });
    expect(wrapper.text()).toContain("Загрузка...");
  });

  it("shows not found when meeting type does not exist", async () => {
    await router.push("/booking/nonexistent");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain("Тип события не найден");
  });

  it("displays meeting type name, description and duration", async () => {
    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain("Consultation");
    expect(wrapper.text()).toContain("30 min meeting");
    expect(wrapper.text()).toContain("30 мин");
  });

  it("renders calendar header with month name and year", async () => {
    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    // June 2026
    expect(wrapper.text()).toContain("Июнь");
    expect(wrapper.text()).toContain("2026");
  });

  it("renders day-of-week headers", async () => {
    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    const dayHeaders = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"];
    for (const dh of dayHeaders) {
      expect(wrapper.text()).toContain(dh);
    }
  });

  it("shows placeholder when no date selected", async () => {
    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain("Выберите дату в календаре");
  });

  it("loads slots when a date is clicked", async () => {
    (getSlots as Mock).mockResolvedValue({ type: "success", data: mockSlots });

    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    // Find an available date button and click it
    // June 13 2026 is Saturday, so the first available weekday is Monday June 15
    const dateButtons = wrapper.findAll("button");
    // Filter for buttons that are day numbers (not nav arrows or back button)
    const dayButton = dateButtons.find(
      (b) => b.text().trim() === "15" && b.classes().includes("text-gray-800")
    );
    expect(dayButton).toBeTruthy();
    await dayButton!.trigger("click");

    expect(getSlots).toHaveBeenCalledWith("2026-06-15", "mt-1");
  });

  it("shows loading state while fetching slots", async () => {
    (getSlots as Mock).mockImplementation(
      () => new Promise(() => {})
    );

    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    const dateButtons = wrapper.findAll("button");
    const dayButton = dateButtons.find(
      (b) => b.text().trim() === "15"
    );
    await dayButton!.trigger("click");
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain("Загрузка слотов");
  });

  it("shows error message when slot fetch fails", async () => {
    (getSlots as Mock).mockResolvedValue({
      type: "failure",
      error: "Server error",
      code: "INTERNAL",
    });

    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    const dateButtons = wrapper.findAll("button");
    const dayButton = dateButtons.find(
      (b) => b.text().trim() === "15"
    );
    await dayButton!.trigger("click");
    await new Promise(process.nextTick);

    expect(wrapper.text()).toContain("Server error");
  });

  it("shows no slots message when slots are empty", async () => {
    (getSlots as Mock).mockResolvedValue({ type: "success", data: [] });

    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    const dateButtons = wrapper.findAll("button");
    const dayButton = dateButtons.find(
      (b) => b.text().trim() === "15"
    );
    await dayButton!.trigger("click");
    await new Promise(process.nextTick);

    expect(wrapper.text()).toContain("Нет доступных слотов");
  });

  it("renders slot buttons when slots are loaded", async () => {
    (getSlots as Mock).mockResolvedValue({ type: "success", data: mockSlots });

    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    const dateButtons = wrapper.findAll("button");
    const dayButton = dateButtons.find(
      (b) => b.text().trim() === "15"
    );
    await dayButton!.trigger("click");
    await new Promise(process.nextTick);

    expect(wrapper.text()).toContain("09:00");
    expect(wrapper.text()).toContain("10:00");
  });

  it("shows booking form when slot is clicked", async () => {
    (getSlots as Mock).mockResolvedValue({ type: "success", data: mockSlots });

    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    // Select date
    const dateButtons = wrapper.findAll("button");
    const dayButton = dateButtons.find(
      (b) => b.text().trim() === "15"
    );
    await dayButton!.trigger("click");
    await new Promise(process.nextTick);

    // Click first slot
    const slotButtons = wrapper.findAll("button");
    const slotButton = slotButtons.find((b) => b.text().includes("09:00"));
    await slotButton!.trigger("click");
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain("Ваше имя");
    expect(wrapper.find('input[type="text"]').exists()).toBe(true);
    expect(wrapper.text()).toContain("Записаться");
  });

  it("validates empty name on submit", async () => {
    (getSlots as Mock).mockResolvedValue({ type: "success", data: mockSlots });

    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    // Select date + click slot
    const dateButtons = wrapper.findAll("button");
    const dayButton = dateButtons.find((b) => b.text().trim() === "15");
    await dayButton!.trigger("click");
    await new Promise(process.nextTick);

    const slotButtons = wrapper.findAll("button");
    const slotButton = slotButtons.find((b) => b.text().includes("09:00"));
    await slotButton!.trigger("click");
    await wrapper.vm.$nextTick();

    // Submit with empty name
    const form = wrapper.find("form");
    await form.trigger("submit");

    expect(wrapper.text()).toContain("Укажите ваше имя");
    expect(createBooking).not.toHaveBeenCalled();
  });

  it("calls createBooking on form submit", async () => {
    (getSlots as Mock).mockResolvedValue({ type: "success", data: mockSlots });
    (createBooking as Mock).mockResolvedValue({
      type: "success",
      data: mockBookingResult,
    });

    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    // Select date
    const dateButtons = wrapper.findAll("button");
    const dayButton = dateButtons.find((b) => b.text().trim() === "15");
    await dayButton!.trigger("click");
    await new Promise(process.nextTick);

    // Click slot
    const slotButtons = wrapper.findAll("button");
    const slotButton = slotButtons.find((b) => b.text().includes("09:00"));
    await slotButton!.trigger("click");
    await wrapper.vm.$nextTick();

    // Fill name and submit
    const input = wrapper.find('input[type="text"]');
    await input.setValue("John");
    const form = wrapper.find("form");
    await form.trigger("submit");
    await new Promise(process.nextTick);

    expect(createBooking).toHaveBeenCalledWith({
      meeting_type_id: "mt-1",
      guest_name: "John",
      start_time: "2026-06-15T09:00:00",
    });
  });

  it("shows confirmation on successful booking", async () => {
    (getSlots as Mock).mockResolvedValue({ type: "success", data: mockSlots });
    (createBooking as Mock).mockResolvedValue({
      type: "success",
      data: mockBookingResult,
    });

    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    // Select date
    const dateButtons = wrapper.findAll("button");
    const dayButton = dateButtons.find((b) => b.text().trim() === "15");
    await dayButton!.trigger("click");
    await new Promise(process.nextTick);

    // Click slot
    const slotButtons = wrapper.findAll("button");
    const slotButton = slotButtons.find((b) => b.text().includes("09:00"));
    await slotButton!.trigger("click");
    await wrapper.vm.$nextTick();

    // Fill and submit
    const input = wrapper.find('input[type="text"]');
    await input.setValue("John");
    const form = wrapper.find("form");
    await form.trigger("submit");
    await new Promise(process.nextTick);

    expect(wrapper.text()).toContain("Вы записаны!");
    expect(wrapper.text()).toContain("John");
    expect(wrapper.text()).toContain("09:00");
  });

  it("navigates back to booking list on back button click", async () => {
    await router.push("/booking/mt-1");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();

    const push = vi.spyOn(router, "push");
    const backButton = wrapper.find("button");
    await backButton.trigger("click");

    expect(push).toHaveBeenCalledWith("/booking");
  });
});
