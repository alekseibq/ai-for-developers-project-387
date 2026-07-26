import { ref } from "vue";
import { defineStore } from "pinia";
import { getBreaks, createBreak, deleteBreak } from "@/api/breaks";
import type { BreakDto, CreateBreakRequest } from "@/types/generated";

export const useBreaksStore = defineStore("breaks", () => {
  const breaks = ref<BreakDto[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchBreaks() {
    loading.value = true;
    try {
      const result = await getBreaks();
      if (result.type === "success") {
        breaks.value = result.data;
        error.value = null;
      } else {
        error.value = result.error;
      }
    } catch {
      error.value = "Network error";
    }
    loading.value = false;
  }

  async function create(data: CreateBreakRequest) {
    try {
      return await createBreak(data);
    } catch {
      return { type: "failure" as const, error: "Network error", code: "NETWORK" };
    }
  }

  async function remove(id: string) {
    try {
      return await deleteBreak(id);
    } catch {
      return { type: "failure" as const, error: "Network error", code: "NETWORK" };
    }
  }

  return { breaks, loading, error, fetchBreaks, create, remove };
});
