import { ref, onUnmounted } from "vue";
import { defineStore } from "pinia";
import { getHealth } from "@/api/client";
import type { HealthResponse } from "@/types/generated";

export const useHealthStore = defineStore("health", () => {
  const health = ref<HealthResponse | null>(null);
  const error = ref<string | null>(null);
  const loading = ref(false);

  let intervalId: ReturnType<typeof setInterval> | null = null;

  async function fetchHealth() {
    loading.value = true;
    try {
      const result = await getHealth();
      if (result.type === "success") {
        health.value = result.data;
        error.value = null;
      } else {
        error.value = result.error;
        health.value = null;
      }
    } catch {
      error.value = "Network error";
      health.value = null;
    }
    loading.value = false;
  }

  function startPolling(ms = 5000) {
    void fetchHealth();
    intervalId = setInterval(fetchHealth, ms);
  }

  function stopPolling() {
    if (intervalId !== null) {
      clearInterval(intervalId);
      intervalId = null;
    }
  }

  onUnmounted(stopPolling);

  return { health, error, loading, fetchHealth, startPolling, stopPolling };
});
