<script setup lang="ts">
import { onMounted, computed } from "vue";
import { useBookingsStore } from "@/stores/bookings";
import type { BookingRichDto } from "@/types/generated";
import { formatDayHeader, formatTime, formatDuration } from "@/utils/date";

const store = useBookingsStore();

onMounted(() => {
  void store.fetchBookings();
});

type GroupedBookings = Record<string, BookingRichDto[]>;

const groupedBookings = computed(() => {
  const groups: GroupedBookings = {};
  for (const b of store.bookings) {
    const key = new Date(b.start_time).toLocaleDateString("ru-RU");
    if (!groups[key]) groups[key] = [];
    groups[key].push(b);
  }
  return groups;
});
</script>

<template>
  <div>
    <div class="mb-6">
      <h2 class="text-2xl font-bold">Предстоящие бронирования</h2>
    </div>

    <div v-if="store.loading" class="text-gray-500">Загрузка...</div>

    <div
      v-else-if="store.error"
      class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600"
    >
      {{ store.error }}
    </div>

    <div v-else-if="store.bookings.length === 0" class="text-gray-500">
      Пока нет ни одной брони.
    </div>

    <div v-else class="space-y-8">
      <div v-for="(dayBookings, dateKey) in groupedBookings" :key="dateKey">
        <h3 class="mb-3 text-lg font-semibold text-gray-800">
          {{ formatDayHeader(dayBookings[0].start_time) }}
        </h3>
        <div class="space-y-3">
          <div
            v-for="b in dayBookings"
            :key="b.id"
            class="rounded-lg border border-gray-200 bg-white p-4"
          >
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-900">{{ b.guest_name }}</p>
                <p class="text-sm text-gray-600">{{ b.meeting_type.name }}</p>
              </div>
              <div class="text-right text-sm">
                <p class="text-gray-700">
                  {{ formatTime(b.start_time) }} — {{ formatTime(b.end_time) }}
                </p>
                <p class="text-gray-500">{{ formatDuration(b.meeting_type.duration_minutes) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
