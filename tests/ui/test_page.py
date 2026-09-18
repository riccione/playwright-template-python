import pytest
from playwright.sync_api import Page


def test_homepage_title(page: Page, env_config):
    page.goto(env_config.BASE_URL)
    assert "Playwright" in page.title()


@pytest.mark.xfail(reason="Intentional fail")
def test_intentional_failure(base_page, env_config):
    base_page.page.goto(env_config.BASE_URL)
    pytest.fail("Forcing a report screenshot generation!")
