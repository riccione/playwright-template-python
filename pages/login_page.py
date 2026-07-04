import logging

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage

logger = logging.getLogger("Framework")


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.username_input: Locator = page.get_by_placeholder("Enter Username")
        self.password_input: Locator = page.get_by_placeholder("Enter Password")
        self.login_button: Locator = page.get_by_role("button", name="Log In")
        self.error_message: Locator = page.locator(".error-message-banner")

    def login(self, username: str, password: str) -> None:
        logger.info(f"[Workflow] Attempting login for user: {username}")
        self.safe_fill(self.username_input, username)
        self.safe_fill(self.password_input, password)
        self.login_button.click()

    def get_error_message_text(self) -> str:
        self.error_message.wait_for(state="visible")
        return self.error_message.inner_text()
