import pytest
from playwright.sync_api import Page


def test_homepage_title(page: Page, env_config):
    page.goto(env_config.BASE_URL)
    assert "Playwright" in page.title()


@pytest.mark.xfail(reason="Intentional fail")
def test_homepage_title_negative(page: Page, env_config):
    page.goto(env_config.BASE_URL)
    assert "NOT" in page.title()
