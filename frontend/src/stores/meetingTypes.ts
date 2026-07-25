import { ref } from "vue";
import { defineStore } from "pinia";
import { getMeetingTypes, createMeetingType } from "@/api/meetingTypes";
import type { MeetingType, CreateMeetingTypeRequest } from "@/types/generated";

export const useMeetingTypesStore = defineStore("meetingTypes", () => {
  const meetingTypes = ref<MeetingType[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchMeetingTypes() {
    loading.value = true;
    try {
      const result = await getMeetingTypes();
      if (result.type === "success") {
        meetingTypes.value = result.data;
        error.value = null;
      } else {
        error.value = result.error;
      }
    } catch {
      error.value = "Network error";
    }
    loading.value = false;
  }

  async function create(data: CreateMeetingTypeRequest) {
    try {
      return await createMeetingType(data);
    } catch {
      return { type: "failure" as const, error: "Network error", code: "NETWORK" };
    }
  }

  return { meetingTypes, loading, error, fetchMeetingTypes, create };
});
