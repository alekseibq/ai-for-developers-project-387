import { describe, it, expect } from "vitest";
import { formatDate, formatTime, formatDayHeader, formatDuration } from "@/utils/date";

describe("date utils", () => {
  it("formatDate formats correctly in Russian locale", () => {
    const result = formatDate("2026-06-15T14:00:00");
    expect(result).toContain("15");
    expect(result).toContain("июня");
    expect(result).toContain("2026");
  });

  it("formatTime formats hours and minutes", () => {
    expect(formatTime("2026-06-15T14:00:00")).toBe("14:00");
    expect(formatTime("2026-06-15T09:05:00")).toBe("09:05");
  });

  it("formatDayHeader includes day name", () => {
    const result = formatDayHeader("2026-06-15T14:00:00");

    expect(result).toContain("15");
    expect(result).toContain("июня");
    expect(result).toContain("2026");
    expect(result).toContain("(пн)");
  });

  it("formatDuration displays minutes", () => {
    expect(formatDuration(30)).toBe("30 мин");
    expect(formatDuration(60)).toBe("60 мин");
  });
});
