<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useMeetingTypesStore } from "@/stores/meetingTypes";

const store = useMeetingTypesStore();
const router = useRouter();

onMounted(() => {
  void store.fetchMeetingTypes();
});
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h2 class="text-2xl font-bold">Типы событий</h2>
      <button
        class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700"
        @click="router.push('/admin/meeting_types/new')"
      >
        Создать новый Тип события
      </button>
    </div>

    <div v-if="store.loading" class="text-gray-500">Загрузка...</div>

    <div
      v-else-if="store.error"
      class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600"
    >
      {{ store.error }}
    </div>

    <div v-else-if="store.meetingTypes.length === 0" class="text-gray-500">
      Пока нет ни одного типа события.
    </div>

    <div v-else class="grid gap-4">
      <div
        v-for="mt in store.meetingTypes"
        :key="mt.id"
        class="rounded-lg border border-gray-200 bg-white p-4"
      >
        <div class="flex items-start justify-between">
          <div>
            <h3 class="text-lg font-semibold">{{ mt.name }}</h3>
            <p class="mt-0.5 font-mono text-xs text-gray-400">{{ mt.id }}</p>
            <p class="mt-1 text-sm text-gray-600">{{ mt.description }}</p>
          </div>
          <span
            class="inline-flex items-center gap-1.5 whitespace-nowrap rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="size-3.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            {{ mt.duration_minutes }} мин
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
