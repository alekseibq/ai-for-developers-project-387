import { describe, it, expect } from "vitest";
import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/pages/HomePage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: "/admin",
    component: { template: "<div><router-view /></div>" },
    children: [
      { path: "", redirect: { name: "meeting-types" } },
      {
        path: "meeting_types",
        name: "meeting-types",
        component: { template: "<div>MeetingTypesPage</div>" },
      },
      {
        path: "meeting_types/new",
        name: "create-meeting-type",
        component: { template: "<div>CreateMeetingTypePage</div>" },
      },
      {
        path: "bookings",
        name: "bookings",
        component: { template: "<div>BookingsPage</div>" },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});

describe("router", () => {
  it("has a route named 'home' at /", () => {
    const route = router.resolve("/");
    expect(route.name).toBe("home");
  });

  it("resolves HomePage component for /", () => {
    const route = router.resolve("/");
    expect(route.matched.length).toBe(1);
    expect(route.matched[0].components?.default).toBe(HomePage);
  });

  it("/admin redirects to meeting-types", async () => {
    await router.push("/admin");
    expect(router.currentRoute.value.name).toBe("meeting-types");
  });

  it("/admin/meeting_types resolves to meeting-types route", () => {
    const route = router.resolve("/admin/meeting_types");
    expect(route.name).toBe("meeting-types");
  });

  it("/admin/meeting_types/new resolves to create-meeting-type route", () => {
    const route = router.resolve("/admin/meeting_types/new");
    expect(route.name).toBe("create-meeting-type");
  });

  it("/admin/bookings resolves to bookings route", () => {
    const route = router.resolve("/admin/bookings");
    expect(route.name).toBe("bookings");
  });
});
