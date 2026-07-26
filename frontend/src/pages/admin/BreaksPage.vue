<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useBreaksStore } from "@/stores/breaks";

const store = useBreaksStore();
const router = useRouter();

onMounted(() => {
  void store.fetchBreaks();
});

const dayNames = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];

function dayLabel(dayOfWeek: number): string {
  if (dayOfWeek === -1) return "Каждый день";
  return dayNames[dayOfWeek] ?? String(dayOfWeek);
}

function formatTime(iso: string): string {
  return iso.slice(0, 5);
}

async function handleDelete(id: string) {
  const result = await store.remove(id);
  if (result.type === "success") {
    await store.fetchBreaks();
  }
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h2 class="text-2xl font-bold">Перерывы</h2>
      <button
        class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700"
        @click="router.push('/admin/breaks/new')"
      >
        Создать перерыв
      </button>
    </div>

    <div v-if="store.loading" class="text-gray-500">Загрузка...</div>

    <div
      v-else-if="store.error"
      class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600"
    >
      {{ store.error }}
    </div>

    <div v-else-if="store.breaks.length === 0" class="text-gray-500">
      Пока нет ни одного перерыва.
    </div>

    <div v-else class="grid gap-4">
      <div
        v-for="b in store.breaks"
        :key="b.id"
        class="flex items-center justify-between rounded-lg border border-gray-200 bg-white p-4"
      >
        <div>
          <h3 class="text-lg font-semibold">{{ b.name }}</h3>
          <p class="mt-1 text-sm text-gray-600">
            {{ dayLabel(b.day_of_week) }}, {{ formatTime(b.start_time) }} — {{ formatTime(b.end_time) }}
          </p>
        </div>
        <button
          class="rounded-md px-3 py-1.5 text-sm font-medium text-red-600 transition-colors hover:bg-red-50"
          @click="handleDelete(b.id)"
        >
          Удалить
        </button>
      </div>
    </div>
  </div>
</template>
