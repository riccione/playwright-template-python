import logging

from playwright.sync_api import Locator, Page

logger = logging.getLogger("Framework")


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input: Locator = page.get_by_placeholder("Enter Username")
        self.password_input: Locator = page.get_by_placeholder("Enter Password")
        self.login_button: Locator = page.get_by_role("button", name="Log In")
        self.error_message: Locator = page.locator(".error-message-banner")

    def login(self, username: str, password: str) -> None:
        logger.info(f"[Workflow] Attempting login for user: {username}")
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
