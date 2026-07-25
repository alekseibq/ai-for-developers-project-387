import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { useBookingsStore } from "@/stores/bookings";
import BookingsPage from "@/pages/admin/BookingsPage.vue";

vi.mock("@/api/bookings", () => ({
  getBookings: vi.fn(),
  createBooking: vi.fn(),
}));

import { getBookings } from "@/api/bookings";
import type { Mock } from "vitest";

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: "/admin",
      component: { template: "<div><router-view /></div>" },
      children: [{ path: "bookings", component: BookingsPage }],
    },
  ],
});

function mountPage() {
  const pinia = createPinia();
  const wrapper = mount(BookingsPage, {
    global: { plugins: [router, pinia] },
  });
  const store = useBookingsStore(pinia);
  return { wrapper, store, pinia };
}

const mockBookings = [
  {
    id: "b1",
    guest_name: "John Doe",
    start_time: "2026-06-15T14:00:00",
    end_time: "2026-06-15T15:00:00",
    created_at: "2026-06-13T12:00:00",
    meeting_type: {
      id: "mt1",
      name: "Consultation",
      description: "60 min meeting",
      duration_minutes: 60,
    },
  },
  {
    id: "b2",
    guest_name: "Jane Smith",
    start_time: "2026-06-15T16:00:00",
    end_time: "2026-06-15T16:30:00",
    created_at: "2026-06-13T12:00:00",
    meeting_type: {
      id: "mt2",
      name: "Quick Call",
      description: "30 min",
      duration_minutes: 30,
    },
  },
];

describe("BookingsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getBookings as Mock).mockResolvedValue({ type: "success", data: [] });
  });

  it("shows loading state", async () => {
    (getBookings as Mock).mockImplementation(() => new Promise(() => {}));

    await router.push("/admin/bookings");
    await router.isReady();

    const { wrapper } = mountPage();
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain("Загрузка...");
  });

  it("shows error message when error is set", async () => {
    (getBookings as Mock).mockResolvedValue({
      type: "failure",
      error: "Failed to load",
      code: "DB_ERROR",
    });

    await router.push("/admin/bookings");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("Failed to load");
  });

  it("shows empty message when no bookings", async () => {
    (getBookings as Mock).mockResolvedValue({ type: "success", data: [] });

    await router.push("/admin/bookings");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("Пока нет ни одной брони");
  });

  it("renders list of bookings grouped by day", async () => {
    (getBookings as Mock).mockResolvedValue({
      type: "success",
      data: mockBookings,
    });

    await router.push("/admin/bookings");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("John Doe");
    expect(wrapper.text()).toContain("Jane Smith");
    expect(wrapper.text()).toContain("Consultation");
    expect(wrapper.text()).toContain("Quick Call");
    expect(wrapper.text()).toContain("60 мин");
    expect(wrapper.text()).toContain("30 мин");
  });

  it("displays day header with date", async () => {
    (getBookings as Mock).mockResolvedValue({
      type: "success",
      data: mockBookings,
    });

    await router.push("/admin/bookings");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("июня");
    expect(wrapper.text()).toContain("(пн)");
  });

  it("shows page title", async () => {
    await router.push("/admin/bookings");
    await router.isReady();

    const { wrapper } = mountPage();
    await new Promise(process.nextTick);
    expect(wrapper.text()).toContain("Предстоящие бронирования");
  });
});
