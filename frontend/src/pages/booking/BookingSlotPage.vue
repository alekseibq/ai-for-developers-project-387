<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import { useMeetingTypesStore } from "@/stores/meetingTypes";
import { getSlots } from "@/api/slots";
import { createBooking } from "@/api/bookings";
import type { SlotDto, BookingRichDto } from "@/types/generated";

const route = useRoute();
const router = useRouter();
const store = useMeetingTypesStore();
const toast = useToast();

const meetingTypeId = route.params.meetingTypeId as string;

const meetingType = computed(
  () => store.meetingTypes.find((mt) => mt.id === meetingTypeId) ?? null,
);

// Today and max booking date
const today = new Date();
today.setHours(0, 0, 0, 0);
const maxDate = new Date(today);
maxDate.setDate(maxDate.getDate() + 13);

// Calendar view state
const viewYear = ref(today.getFullYear());
const viewMonth = ref(today.getMonth());

// Selected date and slots
const selectedDate = ref<string | null>(null);
const slots = ref<SlotDto[]>([]);
const slotsLoading = ref(false);
const slotsError = ref<string | null>(null);

// Selected slot and booking form
const selectedSlot = ref<SlotDto | null>(null);
const guestName = ref("");
const submitting = ref(false);
const bookingResult = ref<BookingRichDto | null>(null);
const nameError = ref<string | null>(null);

// Fetch meeting types if not loaded
onMounted(async () => {
  if (store.meetingTypes.length === 0) {
    await store.fetchMeetingTypes();
  }
});

// Calendar helpers
const dayNames = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"];

const viewMonthName = computed(() => {
  const names = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
  ];
  return names[viewMonth.value];
});

interface CalendarDay {
  day: number;
  date: Date;
  available: boolean;
}

const calendarDays = computed<CalendarDay[]>(() => {
  const days: CalendarDay[] = [];
  const firstDay = new Date(viewYear.value, viewMonth.value, 1);
  const lastDay = new Date(viewYear.value, viewMonth.value + 1, 0);
  const startPad = firstDay.getDay();

  for (let i = 0; i < startPad; i++) {
    const d = new Date(firstDay);
    d.setDate(d.getDate() - (startPad - i));
    days.push({ day: d.getDate(), date: d, available: false });
  }

  for (let d = 1; d <= lastDay.getDate(); d++) {
    const date = new Date(viewYear.value, viewMonth.value, d);
    const isAvailable = isDateAvailable(date);
    days.push({ day: d, date, available: isAvailable });
  }

  return days;
});

function isDateAvailable(date: Date): boolean {
  const day = date.getDay();
  if (day === 0 || day === 6) return false;
  if (date < today) return false;
  if (date > maxDate) return false;
  return true;
}

function canGoPrev(): boolean {
  return (
    viewYear.value > today.getFullYear() ||
    (viewYear.value === today.getFullYear() && viewMonth.value > today.getMonth())
  );
}

function prevMonth() {
  if (viewMonth.value === 0) {
    viewYear.value--;
    viewMonth.value = 11;
  } else {
    viewMonth.value--;
  }
  selectedDate.value = null;
  slots.value = [];
  selectedSlot.value = null;
  bookingResult.value = null;
}

function nextMonth() {
  if (viewMonth.value === 11) {
    viewYear.value++;
    viewMonth.value = 0;
  } else {
    viewMonth.value++;
  }
  selectedDate.value = null;
  slots.value = [];
  selectedSlot.value = null;
  bookingResult.value = null;
}

function formatDateKey(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

function formatDateDisplay(dateStr: string): string {
  const date = new Date(dateStr + "T00:00:00");
  const names = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
  ];
  return `${date.getDate()} ${names[date.getMonth()]} ${date.getFullYear()}`;
}

function formatTime(isoStr: string): string {
  const date = new Date(isoStr);
  const h = String(date.getHours()).padStart(2, "0");
  const m = String(date.getMinutes()).padStart(2, "0");
  return `${h}:${m}`;
}

async function selectDate(date: Date) {
  const dateKey = formatDateKey(date);
  selectedDate.value = dateKey;
  selectedSlot.value = null;
  bookingResult.value = null;
  slotsLoading.value = true;
  slotsError.value = null;

  try {
    const result = await getSlots(dateKey, meetingTypeId);
    if (result.type === "success") {
      slots.value = result.data;
    } else {
      slotsError.value = result.error;
      slots.value = [];
    }
  } catch {
    slotsError.value = "Сервер недоступен. Попробуйте позже.";
    slots.value = [];
  }
  slotsLoading.value = false;
}

function selectSlot(slot: SlotDto) {
  selectedSlot.value = slot;
  guestName.value = "";
  nameError.value = null;
  bookingResult.value = null;
}

function cancelSlotSelection() {
  selectedSlot.value = null;
}

async function submitBooking() {
  if (!guestName.value.trim()) {
    nameError.value = "Укажите ваше имя";
    return;
  }
  nameError.value = null;

  if (!selectedSlot.value || !selectedDate.value) return;

  submitting.value = true;
  try {
    const result = await createBooking({
      meeting_type_id: meetingTypeId,
      guest_name: guestName.value.trim(),
      start_time: selectedSlot.value.start_time,
    });
    if (result.type === "success") {
      bookingResult.value = result.data;
      toast.success("Бронирование создано!");
    } else {
      const messages: Record<string, string> = {
        SLOT_TAKEN: "Это время уже занято. Выберите другой слот.",
        INVALID_GUEST_NAME: "Имя не может быть пустым",
        MEETING_TYPE_NOT_FOUND: "Тип события не найден",
        OUTSIDE_WORK_HOURS: "Время вне рабочих часов",
        OUTSIDE_BOOKING_WINDOW: "Дата вне окна бронирования",
        NETWORK: "Сервер недоступен. Попробуйте позже.",
      };
      const msg = messages[result.code] || result.error || "Произошла ошибка";
      toast.error(msg, { timeout: 8000 });
    }
  } catch {
    toast.error("Сервер недоступен. Попробуйте позже.", { timeout: 8000 });
  }
  submitting.value = false;
}

function resetFlow() {
  selectedDate.value = null;
  slots.value = [];
  selectedSlot.value = null;
  bookingResult.value = null;
  guestName.value = "";
}
</script>

<template>
  <div class="mx-auto max-w-2xl px-4 py-8">
    <button
      class="mb-4 flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      @click="router.push('/booking')"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="size-4"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
      </svg>
      Назад к типам событий
    </button>

    <div v-if="!meetingType && store.loading" class="text-gray-500">Загрузка...</div>

    <div
      v-else-if="!meetingType"
      class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600"
    >
      Тип события не найден
    </div>

    <template v-else>
      <div class="mb-6">
        <h2 class="text-2xl font-bold">{{ meetingType.name }}</h2>
        <p class="mt-1 text-sm text-gray-600">{{ meetingType.description }}</p>
        <span
          class="mt-2 inline-flex items-center gap-1 rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700"
        >
          {{ meetingType.duration_minutes }} мин
        </span>
      </div>

      <div v-if="bookingResult" class="mb-6 rounded-lg border border-green-200 bg-green-50 p-6">
        <h3 class="mb-2 text-lg font-semibold text-green-800">Вы записаны!</h3>
        <div class="space-y-1 text-sm text-green-700">
          <p><span class="font-medium">Имя:</span> {{ bookingResult.guest_name }}</p>
          <p>
            <span class="font-medium">Дата:</span>
            {{ formatDateDisplay(bookingResult.start_time.split("T")[0]) }}
          </p>
          <p>
            <span class="font-medium">Время:</span> {{ formatTime(bookingResult.start_time) }} –
            {{ formatTime(bookingResult.end_time) }}
          </p>
          <p><span class="font-medium">Тип:</span> {{ bookingResult.meeting_type.name }}</p>
        </div>
        <button
          class="mt-4 rounded-md bg-indigo-100 px-4 py-2 text-sm font-medium text-indigo-700 transition-colors hover:bg-indigo-200"
          @click="resetFlow"
        >
          Записаться на другое время
        </button>
      </div>

      <div v-else class="grid grid-cols-1 gap-8 md:grid-cols-2">
        <div>
          <h3 class="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-500">
            Выберите дату
          </h3>

          <div class="rounded-lg border border-gray-200 bg-white p-4">
            <div class="mb-4 flex items-center justify-between">
              <button
                class="p-1 text-gray-400 hover:text-gray-600 disabled:cursor-not-allowed disabled:opacity-30"
                :disabled="!canGoPrev()"
                @click="prevMonth"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="size-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <span class="text-sm font-semibold">{{ viewMonthName }} {{ viewYear }}</span>
              <button class="p-1 text-gray-400 hover:text-gray-600" @click="nextMonth">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="size-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            <div class="grid grid-cols-7 gap-0 text-center">
              <div v-for="dn in dayNames" :key="dn" class="py-1 text-xs font-medium text-gray-400">
                {{ dn }}
              </div>
              <div v-for="(cd, idx) in calendarDays" :key="idx" class="py-1">
                <button
                  v-if="cd.available"
                  class="size-9 rounded-full text-sm font-medium transition-colors"
                  :class="
                    selectedDate === formatDateKey(cd.date)
                      ? 'bg-indigo-600 text-white'
                      : 'text-gray-800 hover:bg-indigo-100'
                  "
                  @click="selectDate(cd.date)"
                >
                  {{ cd.day }}
                </button>
                <span v-else class="inline-block size-9 text-sm leading-9 text-gray-300">
                  {{ cd.day }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div>
          <h3 class="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-500">
            Доступное время
          </h3>

          <div
            v-if="!selectedDate"
            class="rounded-lg border border-dashed border-gray-300 p-6 text-center text-sm text-gray-400"
          >
            Выберите дату в календаре
          </div>

          <div v-else-if="slotsLoading" class="text-sm text-gray-500">Загрузка слотов...</div>

          <div
            v-else-if="slotsError"
            class="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600"
          >
            {{ slotsError }}
          </div>

          <div
            v-else-if="slots.length === 0"
            class="rounded-lg border border-dashed border-gray-300 p-6 text-center text-sm text-gray-400"
          >
            Нет доступных слотов на {{ formatDateDisplay(selectedDate) }}
          </div>

          <div v-else>
            <p class="mb-3 text-sm text-gray-500">
              Доступные слоты на
              <span class="font-medium">{{ formatDateDisplay(selectedDate) }}</span>
            </p>

            <div v-if="!selectedSlot" class="space-y-2">
              <button
                v-for="(slot, idx) in slots"
                :key="idx"
                class="w-full rounded-lg border border-gray-200 px-4 py-3 text-left text-sm font-medium transition-colors hover:border-indigo-300 hover:bg-indigo-50"
                @click="selectSlot(slot)"
              >
                {{ formatTime(slot.start_time) }} – {{ formatTime(slot.end_time) }}
              </button>
            </div>

            <div v-else class="rounded-lg border border-indigo-200 bg-indigo-50 p-4">
              <div class="mb-3 flex items-center justify-between">
                <span class="text-sm font-semibold text-indigo-800">
                  {{ formatTime(selectedSlot.start_time) }} –
                  {{ formatTime(selectedSlot.end_time) }}
                </span>
                <button
                  class="text-xs text-gray-500 underline hover:text-gray-700"
                  @click="cancelSlotSelection"
                >
                  Отменить
                </button>
              </div>

              <form @submit.prevent="submitBooking">
                <div class="mb-3">
                  <label class="mb-1 block text-sm font-medium text-gray-700">Ваше имя</label>
                  <input
                    v-model="guestName"
                    type="text"
                    class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    :class="nameError ? 'border-red-400' : 'border-gray-300'"
                    placeholder="Введите имя"
                  />
                  <p v-if="nameError" class="mt-1 text-xs text-red-500">{{ nameError }}</p>
                </div>
                <button
                  type="submit"
                  :disabled="submitting"
                  class="w-full rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {{ submitting ? "Запись..." : "Записаться" }}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
