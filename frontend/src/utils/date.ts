const DAY_NAMES = ["вс", "пн", "вт", "ср", "чт", "пт", "сб"];

export function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export function formatTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatDayHeader(iso: string): string {
  const d = new Date(iso);
  const dateStr = d.toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  const dayName = DAY_NAMES[d.getDay()];
  return `${dateStr} (${dayName})`;
}

export function formatDuration(minutes: number): string {
  return `${minutes} мин`;
}
