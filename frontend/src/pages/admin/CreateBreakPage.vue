<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import { useBreaksStore } from "@/stores/breaks";

const router = useRouter();
const store = useBreaksStore();
const toast = useToast();

const name = ref("");
const dayOfWeek = ref(0);
const startTime = ref("12:00");
const endTime = ref("13:00");
const submitting = ref(false);
const fieldErrors = ref<Record<string, string>>({});

const dayOptions = [
  { value: -1, label: "Каждый день" },
  { value: 0, label: "Понедельник" },
  { value: 1, label: "Вторник" },
  { value: 2, label: "Среда" },
  { value: 3, label: "Четверг" },
  { value: 4, label: "Пятница" },
  { value: 5, label: "Суббота" },
  { value: 6, label: "Воскресенье" },
];

function validate(): boolean {
  const errors: Record<string, string> = {};
  if (!name.value.trim()) errors.name = "Название обязательно";
  if (!startTime.value) errors.start_time = "Время начала обязательно";
  if (!endTime.value) errors.end_time = "Время окончания обязательно";
  if (startTime.value >= endTime.value) errors.end_time = "Время окончания должно быть позже начала";
  fieldErrors.value = errors;
  return Object.keys(errors).length === 0;
}

async function submit() {
  if (!validate()) return;

  submitting.value = true;
  const result = await store.create({
    name: name.value.trim(),
    day_of_week: dayOfWeek.value,
    start_time: startTime.value,
    end_time: endTime.value,
  });
  submitting.value = false;

  if (result.type === "success") {
    toast.success("Перерыв успешно создан");
    void router.push("/admin/breaks");
  } else {
    const messages: Record<string, string> = {
      INVALID_NAME: "Название не может быть пустым",
      INVALID_DAY_OF_WEEK: "Некорректный день недели",
      INVALID_TIME_RANGE: "Время начала должно быть раньше времени окончания",
      NETWORK: "Сервер недоступен. Попробуйте позже.",
    };
    toast.error(messages[result.code] || result.error || "Произошла ошибка", { timeout: 8000 });
  }
}

function cancel() {
  void router.push("/admin/breaks");
}
</script>

<template>
  <div>
    <h2 class="mb-6 text-2xl font-bold">Создать перерыв</h2>

    <form class="max-w-lg space-y-5" @submit.prevent="submit">
      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">Название</label>
        <input
          v-model="name"
          type="text"
          class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          :class="fieldErrors.name ? 'border-red-400' : 'border-gray-300'"
        />
        <p v-if="fieldErrors.name" class="mt-1 text-xs text-red-500">{{ fieldErrors.name }}</p>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">День недели</label>
        <select
          v-model="dayOfWeek"
          class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option v-for="opt in dayOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Начало</label>
          <input
            v-model="startTime"
            type="time"
            class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            :class="fieldErrors.start_time ? 'border-red-400' : 'border-gray-300'"
          />
          <p v-if="fieldErrors.start_time" class="mt-1 text-xs text-red-500">{{ fieldErrors.start_time }}</p>
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Окончание</label>
          <input
            v-model="endTime"
            type="time"
            class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            :class="fieldErrors.end_time ? 'border-red-400' : 'border-gray-300'"
          />
          <p v-if="fieldErrors.end_time" class="mt-1 text-xs text-red-500">{{ fieldErrors.end_time }}</p>
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
          {{ submitting ? "Создание..." : "Создать" }}
        </button>
      </div>
    </form>
  </div>
</template>
