<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<template>
  <main class="flex min-h-[80vh] flex-col items-center justify-center">
    <h1 class="mb-4 text-4xl font-bold">CalCom</h1>
    <p class="mb-10 max-w-md text-center text-base text-gray-500">
      Сервис для бронирования встреч. Выберите тип встречи и удобное время — гость получит ссылку
      для подтверждения.
    </p>
    <div class="flex gap-6">
      <RouterLink
        to="/booking"
        class="w-48 rounded-lg border border-gray-200 p-6 text-center transition-all duration-200 hover:border-indigo-200 hover:shadow-sm"
      >
        <p class="font-semibold text-gray-800">Забронировать</p>
        <p class="mt-1 text-sm text-gray-500">Перейти к выбору встречи</p>
      </RouterLink>
      <RouterLink
        to="/admin"
        class="w-48 rounded-lg border border-gray-200 p-6 text-center transition-all duration-200 hover:border-indigo-200 hover:shadow-sm"
      >
        <p class="font-semibold text-gray-800">Админка</p>
        <p class="mt-1 text-sm text-gray-500">Управление типами встреч</p>
      </RouterLink>
    </div>
  </main>
</template>
