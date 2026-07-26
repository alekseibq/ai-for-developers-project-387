import { ref } from "vue";
import { defineStore } from "pinia";
import { getHolidays, createHoliday, deleteHoliday } from "@/api/holidays";
import type { HolidayDto, CreateHolidayRequest } from "@/types/generated";

export const useHolidaysStore = defineStore("holidays", () => {
  const holidays = ref<HolidayDto[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchHolidays() {
    loading.value = true;
    try {
      const result = await getHolidays();
      if (result.type === "success") {
        holidays.value = result.data;
        error.value = null;
      } else {
        error.value = result.error;
      }
    } catch {
      error.value = "Network error";
    }
    loading.value = false;
  }

  async function create(data: CreateHolidayRequest) {
    try {
      return await createHoliday(data);
    } catch {
      return { type: "failure" as const, error: "Network error", code: "NETWORK" };
    }
  }

  async function remove(id: string) {
    try {
      return await deleteHoliday(id);
    } catch {
      return { type: "failure" as const, error: "Network error", code: "NETWORK" };
    }
  }

  return { holidays, loading, error, fetchHolidays, create, remove };
});
