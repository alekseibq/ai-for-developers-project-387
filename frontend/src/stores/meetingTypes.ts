import { ref } from "vue";
import { defineStore } from "pinia";
import { getMeetingTypes, getMeetingType, createMeetingType, updateMeetingType } from "@/api/meetingTypes";
import type { MeetingType, CreateMeetingTypeRequest, UpdateMeetingTypeRequest } from "@/types/generated";

export const useMeetingTypesStore = defineStore("meetingTypes", () => {
  const meetingTypes = ref<MeetingType[]>([]);
  const currentMeetingType = ref<MeetingType | null>(null);
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

  async function fetchMeetingType(id: string) {
    loading.value = true;
    currentMeetingType.value = null;
    try {
      const result = await getMeetingType(id);
      if (result.type === "success") {
        currentMeetingType.value = result.data;
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

  async function update(id: string, data: UpdateMeetingTypeRequest) {
    try {
      return await updateMeetingType(id, data);
    } catch {
      return { type: "failure" as const, error: "Network error", code: "NETWORK" };
    }
  }

  return { meetingTypes, currentMeetingType, loading, error, fetchMeetingTypes, fetchMeetingType, create, update };
});
