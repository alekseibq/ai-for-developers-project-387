import { describe, it, expect } from "vitest";
import { mount, RouterLinkStub } from "@vue/test-utils";
import HomePage from "@/pages/HomePage.vue";

describe("HomePage", () => {
  function createWrapper() {
    return mount(HomePage, {
      global: {
        stubs: { RouterLink: RouterLinkStub },
      },
    });
  }

  it("renders the title", () => {
    const wrapper = createWrapper();
    expect(wrapper.text()).toContain("CalCom");
  });

  it("renders the description", () => {
    const wrapper = createWrapper();
    expect(wrapper.text()).toContain("Сервис для бронирования встреч");
  });

  it("renders a link to /booking", () => {
    const wrapper = createWrapper();
    const link = wrapper
      .findAllComponents(RouterLinkStub)
      .find((l) => l.props("to") === "/booking");
    expect(link).toBeDefined();
    expect(link!.text()).toContain("Забронировать");
  });

  it("renders a link to /admin", () => {
    const wrapper = createWrapper();
    const link = wrapper.findAllComponents(RouterLinkStub).find((l) => l.props("to") === "/admin");
    expect(link).toBeDefined();
    expect(link!.text()).toContain("Админка");
  });
});
