<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useHolidaysStore } from "@/stores/holidays";

const store = useHolidaysStore();
const router = useRouter();

onMounted(() => {
  void store.fetchHolidays();
});

function formatDate(iso: string): string {
  const d = new Date(iso + "T00:00:00");
  return d.toLocaleDateString("ru-RU", { day: "numeric", month: "long", year: "numeric" });
}

async function handleDelete(id: string) {
  const result = await store.remove(id);
  if (result.type === "success") {
    await store.fetchHolidays();
  }
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h2 class="text-2xl font-bold">Праздничные дни</h2>
      <button
        class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700"
        @click="router.push('/admin/holidays/new')"
      >
        Добавить праздник
      </button>
    </div>

    <div v-if="store.loading" class="text-gray-500">Загрузка...</div>

    <div
      v-else-if="store.error"
      class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600"
    >
      {{ store.error }}
    </div>

    <div v-else-if="store.holidays.length === 0" class="text-gray-500">
      Пока нет ни одного праздничного дня.
    </div>

    <div v-else class="grid gap-4">
      <div
        v-for="h in store.holidays"
        :key="h.id"
        class="flex items-center justify-between rounded-lg border border-gray-200 bg-white p-4"
      >
        <div>
          <h3 class="text-lg font-semibold">{{ h.name }}</h3>
          <p class="mt-1 text-sm text-gray-600">{{ formatDate(h.date) }}</p>
        </div>
        <button
          class="rounded-md px-3 py-1.5 text-sm font-medium text-red-600 transition-colors hover:bg-red-50"
          @click="handleDelete(h.id)"
        >
          Удалить
        </button>
      </div>
    </div>
  </div>
</template>
