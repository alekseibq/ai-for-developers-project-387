<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import { useMeetingTypesStore } from "@/stores/meetingTypes";

const router = useRouter();
const store = useMeetingTypesStore();
const toast = useToast();

const name = ref("");
const description = ref("");
const durationMinutes = ref<number | null>(null);
const submitting = ref(false);
const fieldErrors = ref<{ name?: string; description?: string; duration_minutes?: string }>({});

function validate(): boolean {
  const errors: typeof fieldErrors.value = {};

  if (!name.value.trim()) {
    errors.name = "Название обязательно";
  }
  if (!description.value.trim()) {
    errors.description = "Описание обязательно";
  }
  if (durationMinutes.value === null || durationMinutes.value < 1) {
    errors.duration_minutes = "Длительность должна быть не менее 1 минуты";
  }

  fieldErrors.value = errors;
  return Object.keys(errors).length === 0;
}

async function submit() {
  if (!validate()) return;

  submitting.value = true;
  const result = await store.create({
    name: name.value.trim(),
    description: description.value.trim(),
    duration_minutes: durationMinutes.value!,
  });
  submitting.value = false;

  if (result.type === "success") {
    toast.success("Тип события успешно создан");
    void router.push("/admin/meeting_types");
  } else {
    const messages: Record<string, string> = {
      INVALID_NAME: "Название не может быть пустым",
      INVALID_DURATION: "Длительность должна быть положительным числом",
      NETWORK: "Сервер недоступен. Попробуйте позже.",
    };
    const userMessage = messages[result.code] || result.error || "Произошла ошибка";
    toast.error(userMessage, {
      timeout: 8000,
    });
  }
}

function cancel() {
  void router.push("/admin/meeting_types");
}
</script>

<template>
  <div>
    <h2 class="mb-6 text-2xl font-bold">Создать новый Тип события</h2>

    <form class="max-w-lg space-y-5" @submit.prevent="submit">
      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">Название</label>
        <input
          v-model="name"
          type="text"
          class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          :class="fieldErrors.name ? 'border-red-400' : 'border-gray-300'"
        />
        <p v-if="fieldErrors.name" class="mt-1 text-xs text-red-500">
          {{ fieldErrors.name }}
        </p>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">Описание</label>
        <textarea
          v-model="description"
          class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          :class="fieldErrors.description ? 'border-red-400' : 'border-gray-300'"
          rows="3"
        />
        <p v-if="fieldErrors.description" class="mt-1 text-xs text-red-500">
          {{ fieldErrors.description }}
        </p>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">
          Длительность (в минутах)
        </label>
        <input
          v-model.number="durationMinutes"
          type="number"
          min="1"
          class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          :class="fieldErrors.duration_minutes ? 'border-red-400' : 'border-gray-300'"
        />
        <p v-if="fieldErrors.duration_minutes" class="mt-1 text-xs text-red-500">
          {{ fieldErrors.duration_minutes }}
        </p>
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
