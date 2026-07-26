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
      {
        path: "breaks",
        name: "breaks",
        component: () => import("@/pages/admin/BreaksPage.vue"),
      },
      {
        path: "breaks/new",
        name: "create-break",
        component: () => import("@/pages/admin/CreateBreakPage.vue"),
      },
      {
        path: "holidays",
        name: "holidays",
        component: () => import("@/pages/admin/HolidaysPage.vue"),
      },
      {
        path: "holidays/new",
        name: "create-holiday",
        component: () => import("@/pages/admin/CreateHolidayPage.vue"),
      },
    ],
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
