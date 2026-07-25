<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from "vue-router";

const route = useRoute();

const navItems = [
  { name: "Типы событий", path: "/admin/meeting_types" },
  { name: "Предстоящие Брони", path: "/admin/bookings" },
];
</script>

<template>
  <div class="flex flex-1">
    <aside class="w-64 border-r border-gray-200 bg-gray-50 p-4 shrink-0">
      <nav class="flex flex-col gap-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
          :class="
            route.path.startsWith(item.path)
              ? 'bg-indigo-100 text-indigo-700'
              : 'text-gray-600 hover:bg-gray-100'
          "
        >
          {{ item.name }}
        </RouterLink>
      </nav>
    </aside>
    <main class="flex-1 p-6">
      <RouterView />
    </main>
  </div>
</template>
