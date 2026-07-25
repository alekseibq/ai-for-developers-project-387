<script setup lang="ts">
import { RouterLink } from "vue-router";
import HealthIndicator from "@/components/HealthIndicator.vue";
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <header
      class="flex items-center justify-between px-6 py-3 border-b border-gray-200 bg-white"
    >
      <div class="flex items-center gap-6">
        <RouterLink to="/" class="text-lg font-semibold hover:underline"
          >CalCom</RouterLink
        >
        <RouterLink
          to="/booking"
          class="text-sm font-medium text-gray-600 hover:text-indigo-600 transition-colors"
          >Забронировать</RouterLink
        >
        <RouterLink
          to="/admin"
          class="text-sm font-medium text-gray-600 hover:text-indigo-600 transition-colors"
          >Админка</RouterLink
        >
      </div>
      <HealthIndicator />
    </header>
    <router-view />
  </div>
</template>
