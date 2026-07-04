import logging

from playwright.sync_api import Locator, Page, Response

logger = logging.getLogger("Framework")


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ---------------------------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------------------------
    def navigate(self, url: str) -> Response | None:
        """Navigate to a specific URL."""
        logger.info(f"Navigating browser window to location: {url}")
        return self.page.goto(url)

    def navigate_to(self, path: str = "") -> Response | None:
        """Navigate to a path relative to the configured baseURL."""
        logger.info(f'[Navigation] Heading to path: "{path}"')
        return self.page.goto(path)

    # ---------------------------------------------------------------------------
    # Wait Helpers
    # ---------------------------------------------------------------------------
    def wait_for_visible(self, locator: Locator, timeout: float = 5000) -> None:
        """Wait for an element to become visible."""
        logger.info(f"Waiting for element to become visible: {locator}")
        locator.wait_for(state="visible", timeout=timeout)

    def wait_for_hidden(self, locator: Locator, timeout: float = 5000) -> None:
        """Wait for an element to become hidden."""
        logger.info(f"Waiting for element to become hidden: {locator}")
        locator.wait_for(state="hidden", timeout=timeout)

    def wait_for_selector(self, selector: str, timeout: float = 5000) -> Locator:
        """Wait for a selector to appear and return the locator."""
        logger.info(f"Waiting for selector: '{selector}'")
        self.page.wait_for_selector(selector, timeout=timeout)
        return self.page.locator(selector)

    # ---------------------------------------------------------------------------
    # Input Helpers
    # ---------------------------------------------------------------------------
    def fill(self, locator: Locator, text: str) -> None:
        """Fill an input field directly (no wait)."""
        logger.info(f"Filling input element with text: '{text}'")
        locator.fill(text)

    def safe_fill(self, locator: Locator, text: str) -> None:
        """Wait for an element to be visible then fill it with text."""
        logger.info(f"Safe-filling input element with text: '{text}'")
        locator.wait_for(state="visible")
        locator.fill(text)

    def type_text(self, locator: Locator, text: str, delay: float = 0) -> None:
        """Type text character by character (useful for inputs with keystroke listeners)."""
        logger.info(f"Typing text into element: '{text}'")
        locator.wait_for(state="visible")
        locator.press_sequentially(text, delay=delay)

    def clear(self, locator: Locator) -> None:
        """Clear an input field."""
        logger.info("Clearing input field")
        locator.wait_for(state="visible")
        locator.clear()

    # ---------------------------------------------------------------------------
    # Click Helpers
    # ---------------------------------------------------------------------------
    def click(self, selector: str, timeout: float = 5000) -> None:
        """Wait for an element to be actionable, then click it by selector."""
        logger.info(f"Performing click interaction on selector element: '{selector}'")
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.click()

    def safe_click(self, locator: Locator, timeout: float = 5000) -> None:
        """Wait for a locator to be visible, then click it."""
        logger.info(f"Performing safe click on element: {locator}")
        locator.wait_for(state="visible", timeout=timeout)
        locator.click()

    # ---------------------------------------------------------------------------
    # Assertion Helpers
    # ---------------------------------------------------------------------------
    def get_text(self, locator: Locator) -> str:
        """Get the inner text of an element."""
        logger.info(f"Retrieving inner text from element: {locator}")
        locator.wait_for(state="visible")
        return locator.inner_text()

    def get_value(self, locator: Locator) -> str:
        """Get the value of an input element."""
        logger.info(f"Retrieving value from input element: {locator}")
        locator.wait_for(state="visible")
        return locator.input_value()

    def is_visible(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        return locator.is_visible()
