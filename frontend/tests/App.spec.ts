import { describe, it, expect, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import App from "@/App.vue";
import HealthIndicator from "@/components/HealthIndicator.vue";

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    { path: "/", name: "home", component: { template: "<div>Home</div>" } },
    {
      path: "/booking",
      component: { template: "<div>Booking</div>" },
    },
    {
      path: "/booking/:meetingTypeId",
      component: { template: "<div>Slot</div>" },
    },
    {
      path: "/admin",
      component: { template: "<div>Admin</div>" },
      children: [
        { path: "", redirect: "/admin/meeting_types" },
        { path: "meeting_types", component: { template: "<div>Types</div>" } },
        { path: "meeting_types/new", component: { template: "<div>New</div>" } },
      ],
    },
  ],
});

describe("App", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("renders CalCom title in header", () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router, createPinia()],
      },
    });

    expect(wrapper.text()).toContain("CalCom");
  });

  it("renders HealthIndicator component", () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router, createPinia()],
      },
    });

    expect(wrapper.findComponent(HealthIndicator).exists()).toBe(true);
  });

  it("renders router-view outlet", () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router, createPinia()],
      },
    });

    expect(wrapper.findComponent({ name: "RouterView" }).exists()).toBe(true);
  });

  it("applies container CSS classes", () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router, createPinia()],
      },
    });

    const container = wrapper.find("div");
    expect(container.classes()).toContain("min-h-screen");
    expect(container.classes()).toContain("flex-col");
  });

  it("renders Админка link in header", () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router, createPinia()],
      },
    });

    expect(wrapper.text()).toContain("Админка");
  });

  it("renders Забронировать link in header", () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router, createPinia()],
      },
    });

    expect(wrapper.text()).toContain("Забронировать");
  });
});
