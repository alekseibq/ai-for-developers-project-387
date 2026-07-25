import { test, expect } from "@playwright/test";

test.describe("Guest booking flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.clock.setFixedTime(new Date("2026-06-13T12:00:00"));
  });
  const meetingTypes = [
    {
      id: "mt-1",
      name: "Consultation",
      description: "30-minute one-on-one",
      duration_minutes: 30,
    },
    {
      id: "mt-2",
      name: "Workshop",
      description: "60-minute group session",
      duration_minutes: 60,
    },
  ];

  const mockSlots = [
    { start_time: "2026-06-15T09:00:00", end_time: "2026-06-15T09:30:00" },
    { start_time: "2026-06-15T10:00:00", end_time: "2026-06-15T10:30:00" },
  ];

  const mockBookingResult = {
    id: "b-1",
    guest_name: "John Doe",
    start_time: "2026-06-15T09:00:00",
    end_time: "2026-06-15T09:30:00",
    created_at: "2026-06-13T12:00:00",
    meeting_type: meetingTypes[0],
  };

  test("happy path: guest selects meeting type, date, slot, and creates booking", async ({
    page,
  }) => {
    await page.route("**/api/v1/meeting-types", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ type: "success", data: meetingTypes }),
      });
    });

    await page.route("**/api/v1/slots*", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ type: "success", data: mockSlots }),
      });
    });

    await page.route("**/api/v1/bookings", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ type: "success", data: mockBookingResult }),
      });
    });

    await page.goto("/booking");
    await page.waitForSelector("text=Consultation");

    // Step 1: See meeting types
    await expect(page.locator("text=Consultation")).toBeVisible();
    await expect(page.locator("text=Workshop")).toBeVisible();
    await expect(page.locator("text=30 мин")).toBeVisible();
    await expect(page.locator("text=60 мин")).toBeVisible();

    // Step 2: Click on Consultation
    await page.locator("text=Consultation").click();
    await page.waitForURL("**/booking/mt-1");

    // Step 3: See meeting type details and calendar
    await expect(page.locator("text=30-minute one-on-one")).toBeVisible();
    await expect(page.locator("text=Июнь 2026")).toBeVisible();

    // Step 4: Click on an available date (June 15 = Monday)
    // Find the day "15" in the calendar that is clickable
    const day15 = page.locator("button", { hasText: "15" }).first();
    await day15.click();

    // Step 5: See slots and click one
    await expect(page.locator("text=09:00")).toBeVisible({ timeout: 10000 });
    await page.locator("text=09:00").click();

    // Step 6: Fill name and submit
    await expect(page.locator("text=Ваше имя")).toBeVisible();
    await page.fill("input[type='text']", "John Doe");
    await page.locator("text=Записаться").click();

    // Step 7: See success confirmation
    await expect(page.locator("text=Вы записаны!")).toBeVisible({ timeout: 10000 });
    await expect(page.locator("text=John Doe")).toBeVisible();
    await expect(page.locator("text=09:00")).toBeVisible();
  });

  test("shows empty state when no meeting types exist", async ({ page }) => {
    await page.route("**/api/v1/meeting-types", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ type: "success", data: [] }),
      });
    });

    await page.goto("/booking");

    await expect(page.locator("text=Пока нет ни одного типа события")).toBeVisible();
  });

  test("shows no slots message when no slots are available", async ({ page }) => {
    await page.route("**/api/v1/meeting-types", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ type: "success", data: meetingTypes }),
      });
    });

    await page.route("**/api/v1/slots*", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ type: "success", data: [] }),
      });
    });

    await page.goto("/booking");
    await page.waitForSelector("text=Consultation");
    await page.locator("text=Consultation").click();

    const day15 = page.locator("button", { hasText: "15" }).first();
    await day15.click();

    await expect(page.locator("text=Нет доступных слотов")).toBeVisible({ timeout: 10000 });
  });

  test("shows error toast when booking fails with SLOT_TAKEN", async ({ page }) => {
    await page.route("**/api/v1/meeting-types", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ type: "success", data: meetingTypes }),
      });
    });

    await page.route("**/api/v1/slots*", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ type: "success", data: mockSlots }),
      });
    });

    await page.route("**/api/v1/bookings", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          type: "failure",
          error: "Slot is already taken",
          code: "SLOT_TAKEN",
        }),
      });
    });

    await page.goto("/booking");
    await page.waitForSelector("text=Consultation");
    await page.locator("text=Consultation").click();

    const day15 = page.locator("button", { hasText: "15" }).first();
    await day15.click();
    await page.locator("text=09:00").click({ timeout: 10000 });
    await page.fill("input[type='text']", "John Doe");
    await page.locator("text=Записаться").click();

    await expect(page.locator("text=Это время уже занято")).toBeVisible({ timeout: 10000 });
  });

  test("navigates from header link to booking page", async ({ page }) => {
    await page.route("**/api/v1/meeting-types", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ type: "success", data: [] }),
      });
    });

    await page.goto("/");

    // Click "Забронировать" in header (not the home page tile)
    await page.locator("header a", { hasText: "Забронировать" }).click();
    await page.waitForURL("/booking");

    await expect(page.locator("text=Выберите тип события")).toBeVisible();
  });
});
