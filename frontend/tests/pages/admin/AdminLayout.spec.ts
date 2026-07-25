import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from "pinia";
import AdminLayout from "@/pages/admin/AdminLayout.vue";

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: "/admin",
      component: AdminLayout,
      children: [
        { path: "", redirect: "/admin/meeting_types" },
        { path: "meeting_types", component: { template: "<div>List</div>" } },
        { path: "bookings", component: { template: "<div>Bookings</div>" } },
      ],
    },
  ],
});

describe("AdminLayout", () => {
  it("renders sidebar with two navigation items", async () => {
    await router.push("/admin/meeting_types");
    await router.isReady();

    const wrapper = mount(AdminLayout, {
      global: { plugins: [router, createPinia()] },
    });

    expect(wrapper.text()).toContain("Типы событий");
    expect(wrapper.text()).toContain("Предстоящие Брони");
  });

  it("renders router-view outlet", async () => {
    await router.push("/admin/meeting_types");
    await router.isReady();

    const wrapper = mount(AdminLayout, {
      global: { plugins: [router, createPinia()] },
    });

    expect(wrapper.findComponent({ name: "RouterView" }).exists()).toBe(true);
  });

  it("highlights the meeting_types link when on that page", async () => {
    await router.push("/admin/meeting_types");
    await router.isReady();

    const wrapper = mount(AdminLayout, {
      global: { plugins: [router, createPinia()] },
    });

    const links = wrapper.findAll("a");
    expect(links[0].classes()).toContain("bg-indigo-100");
    expect(links[1].classes()).not.toContain("bg-indigo-100");
  });

  it("highlights the bookings link when on that page", async () => {
    await router.push("/admin/bookings");
    await router.isReady();

    const wrapper = mount(AdminLayout, {
      global: { plugins: [router, createPinia()] },
    });

    const links = wrapper.findAll("a");
    expect(links[0].classes()).not.toContain("bg-indigo-100");
    expect(links[1].classes()).toContain("bg-indigo-100");
  });
});
