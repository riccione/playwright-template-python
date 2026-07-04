import pytest

from pages.base_page import BasePage


def test_homepage_title(base_page: BasePage):
    base_page.page.goto("https://playwright.dev/")
    assert "Playwright" in base_page.page.title()


@pytest.mark.xfail(reason="Intentional fail")
def test_intentional_failure(base_page, env_config):
    base_page.page.goto(env_config.BASE_URL)
    pytest.fail("Forcing a report screenshot generation!")
