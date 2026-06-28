import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage


@pytest.fixture
def base_page(page: Page) -> BasePage:
    """Provides a fresh instance of BasePage using Playwright's built-in page fixture."""
    return BasePage(page)


@pytest.fixture(scope="function")
def authenticated_session(page: Page, env_config):
    """
    Pre-configures a fresh state for a single test.
    scope="function" means it runs once per test function.
    """
    # ------------------ SETUP ------------------
    print(f"\n[Test Setup] Injecting default state or routing to {env_config.BASE_URL}")
    page.goto(env_config.BASE_URL)

    # Example: Injecting a cookie or storage state to stay logged in
    # page.context.add_cookies([{"name": "session_id", "value": "xyz", "url": env_config.BASE_URL}])

    yield page  # Passes the clean, ready-to-use page object to the test

    # ----------------- TEARDOWN -----------------
    print("\n[Test Teardown] Clearing browser storage and resetting cookies...")
    try:
        page.context.clear_cookies()
        page.evaluate("window.localStorage.clear();")
    except Exception:
        pass  # Browser might already be closed by reporting hooks on failure
