import { createPinia, setActivePinia } from "pinia";
import { beforeEach } from "vitest";
import { config } from "@vue/test-utils";

const consoleWarn = console.warn;
console.warn = (msg, ...args) => {
  if (typeof msg === "string" && msg.includes("onUnmounted")) return;
  consoleWarn(msg, ...args);
};

beforeEach(() => {
  setActivePinia(createPinia());
});
