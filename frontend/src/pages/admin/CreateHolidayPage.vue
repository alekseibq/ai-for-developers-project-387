<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import { useHolidaysStore } from "@/stores/holidays";

const router = useRouter();
const store = useHolidaysStore();
const toast = useToast();

const name = ref("");
const date = ref("");
const submitting = ref(false);
const fieldErrors = ref<Record<string, string>>({});

function validate(): boolean {
  const errors: Record<string, string> = {};
  if (!name.value.trim()) errors.name = "Название обязательно";
  if (!date.value) errors.date = "Дата обязательна";
  fieldErrors.value = errors;
  return Object.keys(errors).length === 0;
}

async function submit() {
  if (!validate()) return;

  submitting.value = true;
  const result = await store.create({
    name: name.value.trim(),
    date: date.value,
  });
  submitting.value = false;

  if (result.type === "success") {
    toast.success("Праздничный день добавлен");
    void router.push("/admin/holidays");
  } else {
    const messages: Record<string, string> = {
      INVALID_NAME: "Название не может быть пустым",
      NETWORK: "Сервер недоступен. Попробуйте позже.",
    };
    toast.error(messages[result.code] || result.error || "Произошла ошибка", { timeout: 8000 });
  }
}

function cancel() {
  void router.push("/admin/holidays");
}
</script>

<template>
  <div>
    <h2 class="mb-6 text-2xl font-bold">Добавить праздничный день</h2>

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
        <label class="mb-1 block text-sm font-medium text-gray-700">Дата</label>
        <input
          v-model="date"
          type="date"
          class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          :class="fieldErrors.date ? 'border-red-400' : 'border-gray-300'"
        />
        <p v-if="fieldErrors.date" class="mt-1 text-xs text-red-500">{{ fieldErrors.date }}</p>
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
          {{ submitting ? "Добавление..." : "Добавить" }}
        </button>
      </div>
    </form>
  </div>
</template>
