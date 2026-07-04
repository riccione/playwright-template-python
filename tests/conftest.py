import base64
import logging
import os
from datetime import datetime

import pytest

from config import settings

logger = logging.getLogger("Framework")

# Try importing allure safely, if not installed or used it won't crash
try:
    import allure
except ImportError:
    allure = None

# Load fixtures from fixtures module
pytest_plugins = [
    "fixtures.page_fixtures",
]


@pytest.fixture(scope="session")
def env_config():
    """Provides centralized .env configuration settings to tests."""
    return settings


def pytest_configure(config):
    """Dynamically sets HTML report filename with a timestamp."""
    # Ensure a 'reports' directory exists
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Generate timestamp (e.g., 2026-06-27_17-15-30)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"report_{timestamp}.html"

    # Set the path dynamically for the html plugin
    config.option.htmlpath = os.path.join(reports_dir, report_name)


# ==============================================================================
# HOOK: GENERATING METADATA AND CAPTURING FAILURES
# ==============================================================================
# tryfirst=True ensures this hook runs before other plugins modify execution data.
# hookwrapper=True allows us to wrap the standard execution phase so we can inspect outcome
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Universal hook that attaches screenshots and videos to Allure 3 or Pytest-HTML on failure."""
    outcome = yield
    report = outcome.get_result()

    if not hasattr(report, "extras"):
        report.extras = []

    # Filter for failures inside the primary test execution step
    if report.when == "call" and report.failed:
        # Locate the running Playwright browser tab instance
        page_instance = None
        if "base_page" in item.funcargs:
            page_instance = item.funcargs["base_page"].page
        elif "page" in item.funcargs:
            page_instance = item.funcargs["page"]

        if page_instance:
            # ATTACH FAILURE SCREENSHOTS
            try:
                screenshot_bytes = page_instance.screenshot(full_page=True)

                # A: Send directly to Allure 3
                if allure and item.config.getoption("--alluredir", default=None):
                    allure.attach(
                        screenshot_bytes,
                        name="Failure Screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )

                # B: Backup mapping for plain Pytest-HTML
                from pytest_html import extras

                b64_img = base64.b64encode(screenshot_bytes).decode("utf-8")
                report.extras.append(extras.png(b64_img))
            except Exception as e:
                logger.error(f"Failed to attach screenshot: {e}")

            # ATTACH FAILURE VIDEOS
            try:
                # Explicitly close context to finalize video buffering blocks on disk
                page_instance.context.close()

                if page_instance.video:
                    video_path = page_instance.video.path()

                    if os.path.exists(video_path):
                        with open(video_path, "rb") as video_file:
                            video_bytes = video_file.read()

                        # A: Stream into the Allure 3 dashboard environment
                        if allure and item.config.getoption("--alluredir", default=None):
                            allure.attach(
                                video_bytes,
                                name="Failure Video Recording",
                                attachment_type=allure.attachment_type.WEBM,
                            )

                        # B: Map relative link path for plain Pytest-HTML
                        relative_path = os.path.relpath(video_path, start=os.getcwd())
                        from pytest_html import extras

                        report.extras.append(
                            extras.url(f"../{relative_path}", name="Watch Failure Video")
                        )
            except Exception as e:
                logger.error(f"Failed to handle video capture processing: {e}")


# ==============================================================================
# GLOBAL SETUP & TEARDOWN
# ==============================================================================
@pytest.fixture(scope="session", autouse=True)
def global_system_lifecycle():
    """
    Global Setup & Teardown blueprint.
    scope="session" means it runs once for the entire test run.
    autouse=True means every test session runs it automatically.
    """
    # ------------------ SETUP ------------------
    logger.info("=" * 70)
    logger.info("[GLOBAL SETUP] Booting test execution session...")
    logger.info(f"[GLOBAL SETUP] Base URL target configured as: {settings.BASE_URL}")
    logger.info("=" * 70)

    # Place global hooks here (e.g., seeding a database, Docker init, global auth)

    yield  # <--- This is where the tests actually execute!

    # ----------------- TEARDOWN -----------------
    logger.info("=" * 70)
    logger.info("[GLOBAL TEARDOWN] Test suite execution loop completed.")
    logger.info("[GLOBAL TEARDOWN] Purging temporary run artifacts and memory buffers...")
    logger.info("=" * 70)

    # Place global cleanups here (e.g., tearing down testing infrastructure, dropping DB records)
