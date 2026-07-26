<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import { useMeetingTypesStore } from "@/stores/meetingTypes";
import type { BreakDto, HolidayDto } from "@/types/generated";

const route = useRoute();
const router = useRouter();
const store = useMeetingTypesStore();
const toast = useToast();

const meetingTypeId = route.params.meetingTypeId as string;

const name = ref("");
const description = ref("");
const durationMinutes = ref<number | null>(null);
const workingHoursStart = ref("09:00");
const workingHoursEnd = ref("18:00");
const breaks = ref<BreakDto[]>([]);
const holidays = ref<HolidayDto[]>([]);
const submitting = ref(false);

const newBreakStart = ref("12:00");
const newBreakEnd = ref("13:00");
const newHolidayDate = ref("");
const newHolidayName = ref("");

onMounted(async () => {
  await store.fetchMeetingType(meetingTypeId);
  if (store.currentMeetingType) {
    const mt = store.currentMeetingType;
    name.value = mt.name;
    description.value = mt.description;
    durationMinutes.value = mt.duration_minutes;
    workingHoursStart.value = mt.working_hours_start;
    workingHoursEnd.value = mt.working_hours_end;
    breaks.value = mt.breaks.map((b) => ({ ...b }));
    holidays.value = mt.holidays.map((h) => ({ ...h }));
  }
});

function addBreak() {
  breaks.value.push({
    start_time: newBreakStart.value,
    end_time: newBreakEnd.value,
  });
}

function removeBreak(index: number) {
  breaks.value.splice(index, 1);
}

function addHoliday() {
  if (!newHolidayDate.value) return;
  holidays.value.push({
    date: newHolidayDate.value,
    name: newHolidayName.value.trim() || "Праздничный день",
  });
  newHolidayDate.value = "";
  newHolidayName.value = "";
}

function removeHoliday(index: number) {
  holidays.value.splice(index, 1);
}

async function submit() {
  if (!name.value.trim()) {
    toast.error("Название обязательно");
    return;
  }
  if (durationMinutes.value === null || durationMinutes.value < 1) {
    toast.error("Длительность должна быть положительным целым числом");
    return;
  }

  submitting.value = true;
  const result = await store.update(meetingTypeId, {
    name: name.value.trim(),
    description: description.value.trim(),
    duration_minutes: durationMinutes.value,
    working_hours_start: workingHoursStart.value,
    working_hours_end: workingHoursEnd.value,
    breaks: breaks.value,
    holidays: holidays.value,
  });
  submitting.value = false;

  if (result.type === "success") {
    toast.success("Тип события обновлён");
    void router.push("/admin/meeting_types");
  } else {
    const messages: Record<string, string> = {
      INVALID_NAME: "Название не может быть пустым",
      INVALID_DURATION: "Длительность должна быть положительным целым числом",
      NETWORK: "Сервер недоступен. Попробуйте позже.",
    };
    toast.error(messages[result.code] || result.error || "Произошла ошибка", { timeout: 8000 });
  }
}

function cancel() {
  void router.push("/admin/meeting_types");
}
</script>

<template>
  <div>
    <h2 class="mb-6 text-2xl font-bold">Настройка типа события</h2>

    <div v-if="store.loading" class="text-gray-500">Загрузка...</div>

    <div
      v-else-if="!store.currentMeetingType"
      class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600"
    >
      Тип события не найден
    </div>

    <form v-else class="max-w-2xl space-y-6" @submit.prevent="submit">
      <div class="rounded-lg border border-gray-200 bg-white p-4">
        <h3 class="mb-4 text-lg font-semibold">Основная информация</h3>

        <div class="mb-4">
          <label class="mb-1 block text-sm font-medium text-gray-700">Название</label>
          <input
            v-model="name"
            type="text"
            class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div class="mb-4">
          <label class="mb-1 block text-sm font-medium text-gray-700">Описание</label>
          <textarea
            v-model="description"
            class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            rows="3"
          />
        </div>

        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Длительность (в минутах)</label>
          <input
            v-model.number="durationMinutes"
            type="number"
            min="1"
            class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-4">
        <h3 class="mb-4 text-lg font-semibold">Рабочие часы</h3>

        <div class="flex gap-4">
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Начало</label>
            <input
              v-model="workingHoursStart"
              type="time"
              class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Конец</label>
            <input
              v-model="workingHoursEnd"
              type="time"
              class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-4">
        <h3 class="mb-4 text-lg font-semibold">Перерывы</h3>

        <div v-if="breaks.length === 0" class="mb-3 text-sm text-gray-400">
          Перерывы не заданы
        </div>

        <div v-for="(b, idx) in breaks" :key="idx" class="mb-2 flex items-center gap-3">
          <span class="text-sm text-gray-600">
            {{ b.start_time }} – {{ b.end_time }}
          </span>
          <button
            type="button"
            class="text-xs text-red-500 hover:text-red-700"
            @click="removeBreak(idx)"
          >
            Удалить
          </button>
        </div>

        <div class="mt-3 flex items-center gap-2">
          <input
            v-model="newBreakStart"
            type="time"
            class="rounded-md border border-gray-300 px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <span class="text-sm text-gray-500">–</span>
          <input
            v-model="newBreakEnd"
            type="time"
            class="rounded-md border border-gray-300 px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            type="button"
            class="rounded-md bg-indigo-100 px-3 py-1.5 text-sm font-medium text-indigo-700 hover:bg-indigo-200"
            @click="addBreak"
          >
            Добавить
          </button>
        </div>
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-4">
        <h3 class="mb-4 text-lg font-semibold">Праздничные дни</h3>

        <div v-if="holidays.length === 0" class="mb-3 text-sm text-gray-400">
          Праздничные дни не заданы
        </div>

        <div v-for="(h, idx) in holidays" :key="idx" class="mb-2 flex items-center gap-3">
          <span class="text-sm text-gray-600">{{ h.date }}</span>
          <span v-if="h.name" class="text-sm text-gray-500">– {{ h.name }}</span>
          <button
            type="button"
            class="text-xs text-red-500 hover:text-red-700"
            @click="removeHoliday(idx)"
          >
            Удалить
          </button>
        </div>

        <div class="mt-3 flex items-center gap-2">
          <input
            v-model="newHolidayDate"
            type="date"
            class="rounded-md border border-gray-300 px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <input
            v-model="newHolidayName"
            type="text"
            placeholder="Название"
            class="rounded-md border border-gray-300 px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            type="button"
            class="rounded-md bg-indigo-100 px-3 py-1.5 text-sm font-medium text-indigo-700 hover:bg-indigo-200"
            @click="addHoliday"
          >
            Добавить
          </button>
        </div>
      </div>

      <div class="flex gap-3 pt-2">
        <button
          type="button"
          class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
          @click="cancel"
        >
          Отменить
        </button>
        <button
          type="submit"
          :disabled="submitting"
          class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ submitting ? "Сохранение..." : "Сохранить" }}
        </button>
      </div>
    </form>
  </div>
</template>
