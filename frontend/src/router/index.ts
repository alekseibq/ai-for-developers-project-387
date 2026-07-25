import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/pages/HomePage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: "/booking",
    name: "booking",
    component: () => import("@/pages/booking/BookingMeetingTypesPage.vue"),
  },
  {
    path: "/booking/:meetingTypeId",
    name: "booking-slots",
    component: () => import("@/pages/booking/BookingSlotPage.vue"),
  },
  {
    path: "/admin",
    component: () => import("@/pages/admin/AdminLayout.vue"),
    children: [
      {
        path: "",
        redirect: { name: "meeting-types" },
      },
      {
        path: "meeting_types",
        name: "meeting-types",
        component: () => import("@/pages/admin/MeetingTypesPage.vue"),
      },
      {
        path: "meeting_types/new",
        name: "create-meeting-type",
        component: () => import("@/pages/admin/CreateMeetingTypePage.vue"),
      },
      {
        path: "bookings",
        name: "bookings",
        component: () => import("@/pages/admin/BookingsPage.vue"),
      },
    ],
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
