import { test, expect } from "@playwright/test";

test.describe("Health indicator", () => {
  test("shows green dot and status text when backend is healthy", async ({ page }) => {
    await page.route("**/api/v1/health", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          type: "success",
          data: {
            status: "ok",
            version: "0.1.0",
            database: "connected",
            uptime: 42,
          },
        }),
      });
    });

    await page.goto("/");

    await expect(page.locator(".bg-green-500")).toBeVisible({
      timeout: 15000,
    });
    await expect(page.getByText(/ok · v/)).toBeVisible();
  });

  test("shows offline when backend is unreachable", async ({ page }) => {
    await page.route("**/api/v1/health", async (route) => {
      await route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ type: "failure", error: "Server error", code: "INTERNAL" }),
      });
    });

    await page.goto("/");

    await expect(page.getByText("offline")).toBeVisible({ timeout: 10000 });
  });

  test("shows degraded when backend reports degraded", async ({ page }) => {
    await page.route("**/api/v1/health", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          type: "success",
          data: {
            status: "degraded",
            version: "0.1.0",
            database: "disconnected",
            uptime: 42,
          },
        }),
      });
    });

    await page.goto("/");

    await expect(page.locator(".bg-yellow-500")).toBeVisible({
      timeout: 10000,
    });
    await expect(page.getByText(/degraded · v/)).toBeVisible();
  });
});
