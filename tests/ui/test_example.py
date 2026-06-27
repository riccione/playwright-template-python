from playwright.sync_api import Page

def test_homepage_title(page):
    page.goto("https://playwright.dev/")
    assert "Playwright" in page.title()
