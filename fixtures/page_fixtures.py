import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Provides a fresh instance of LoginPage using Playwright's built-in page fixture."""
    return LoginPage(page)
