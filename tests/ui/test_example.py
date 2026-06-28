from playwright.sync_api import Page


def test_homepage_title(page: Page):
    page.goto("https://playwright.dev/")
    assert "Playwright" in page.title()


def test_homepage_title_negative(page: Page):
    page.goto("https://playwright.dev/")
    assert "NOT" in page.title()
