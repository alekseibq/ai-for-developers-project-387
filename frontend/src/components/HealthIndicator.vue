<script setup lang="ts">
import { onMounted } from "vue";
import { useHealthStore } from "@/stores/health";

const store = useHealthStore();

onMounted(() => {
  store.startPolling();
});

function dotColor(): string {
  if (store.error) return "bg-red-500";
  if (store.health?.status === "ok") return "bg-green-500";
  if (store.health?.status === "degraded") return "bg-yellow-500";
  return "bg-gray-400";
}
</script>

<template>
  <div class="flex items-center gap-2 text-sm">
    <span class="relative flex h-3 w-3">
      <span
        :class="[dotColor(), 'inline-flex h-full w-full rounded-full']"
      ></span>
    </span>
    <span v-if="store.loading" class="text-gray-400">checking...</span>
    <span v-else-if="store.health" class="text-gray-500">
      {{ store.health.status }} · v{{ store.health.version }}
    </span>
    <span v-else-if="store.error" class="text-red-500">offline</span>
  </div>
</template>
