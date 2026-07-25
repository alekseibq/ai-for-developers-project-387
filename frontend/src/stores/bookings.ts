import { defineStore } from "pinia";
import { ref } from "vue";
import { getBookings } from "@/api/bookings";
import type { BookingRichDto } from "@/types/generated";

export const useBookingsStore = defineStore("bookings", () => {
  const bookings = ref<BookingRichDto[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchBookings() {
    loading.value = true;
    error.value = null;
    try {
      const result = await getBookings();
      if (result.type === "success") {
        bookings.value = result.data
          .slice()
          .sort(
            (a: BookingRichDto, b: BookingRichDto) =>
              new Date(a.start_time).getTime() - new Date(b.start_time).getTime(),
          );
        error.value = null;
      } else {
        error.value = result.error;
        bookings.value = [];
      }
    } catch {
      error.value = "Network error";
      bookings.value = [];
    }
    loading.value = false;
  }

  return { bookings, loading, error, fetchBookings };
});
