import logging
from playwright.sync_api import Locator, Page, Response

logger = logging.getLogger("Framework")


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> Response | None:
        logger.info(f"Navigating browser window to location: {url}")
        return self.page.goto(url)

    def safe_fill(self, locator: Locator, text: str) -> None:
        """Waits for an element to be visible then fills it with text."""
        logger.info(f"Filling input element with text: '{text}'")
        locator.wait_for(state="visible")
        locator.fill(text)

    def click(self, selector: str, timeout: float = 5000) -> None:
        """Explicitly waits for an element to be actionable, then clicks it."""
        logger.info(f"Performing click interaction on selector element: '{selector}'")
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.click()
