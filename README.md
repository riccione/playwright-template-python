# Playwright Python Test Automation Framework

A modern, highly optimized End-to-End (E2E) UI testing template using Python,
`pytest`, Playwright, and `uv` for lightning-fast environment dependency
management.

This framework implements a decoupled Page Object Model (POM) architecture,
cross-browser support, test lifecycle tracking, linting quality gates, and dual-reporting capability
(Pytest-HTML & Allure 3) featuring automated screenshot and video capture upon
test failures.

---

## Features

* **Fast Dependency Management**: Driven by `uv` for rapid virtual environment syncs.
* **Page Object Model (POM)**: Fully decoupled architecture separating page selectors from business workflows.
* **Configuration Management**: Centralized `.env` handling via `python-dotenv` to eliminate hardcoded secrets.
* **Code Quality & Enforcement**: Built-in automated linting and formatting via `ruff` backed by `pre-commit` git hooks.
* **Dynamic Dual Reporting**: Built-in compatibility for choosing lightweight `pytest-html` tracking or fully enterprise-grade `Allure 3` visual dashboards.
* **Rich Failure Artifacts**: Automated hook interception captures full-page browser screenshots and saves screen recordings explicitly on test failure conditions.
* **Universal CI/CD Ready**: Native multi-platform workflow blueprints provided out-of-the-box for GitHub Actions, GitLab CI, and Jenkins.

---

## Directory Structure

```text
├── .github/workflows/playwright.yml # GitHub Actions pipeline blueprint
├── .gitlab-ci.yml           # GitLab CI orchestration blueprint
├── .env.example             # Safe template for tracking configuration variables
├── .gitignore               # Strict untracked execution pattern matching
├── .pre-commit-config.yaml  # Intercepts git loops to enforce ruff styling
├── Jenkinsfile              # Jenkins Declarative pipeline engine script
├── LICENSE                  # MIT License agreement
├── pytest.ini               # Root-level configuration file for execution flags
├── pyproject.toml           # Project definitions and package dependencies
├── config.py                # Single source of truth environment parser
├── fixtures/
│   └── page_fixtures.py     # Global Pytest fixtures providing encapsulated page instances
├── pages/
│   ├── base_page.py         # Core Page Object wrapper handling Playwright components
│   └── login_page.py        # Clean workflow extension decoupling logic from selectors
└── tests/
    ├── conftest.py          # Global framework lifecycle hooks, setups, and teardowns
    ├── api/
    │   └── test_api_example.py  # API testing examples with Playwright request context
    ├── regression/          # [.gitkeep] Broad validation execution scripts
    ├── smoke/               # [.gitkeep] High priority critical path milestones
    └── ui/
        ├── test_page.py        # Page Object Model-based UI test suites
        └── test_ui_example.py  # Basic UI testing examples

```

### Project Conventions

This template provides a minimal structure. As your project grows, create dedicated helper directories at the root level alongside `pages/` and `fixtures/`:

| Directory | Purpose |
|---|---|
| `api/` | Reusable API clients, endpoint definitions, request/response models |
| `utils/` | Shared utilities (data generators, wait helpers, custom logging) |
| `helpers/` | Cross-cutting concerns (auth helpers, environment builders) |

```text
# Example of a grown project structure
├── api/
│   ├── client.py           # Reusable HTTP client with auth handling
│   ├── endpoints.py        # URL constants
│   └── models.py           # Pydantic response/request models
├── fixtures/
├── pages/
├── utils/
│   ├── data_generator.py   # Test data factories
│   └── wait_helpers.py     # Custom wait conditions
└── tests/
```

Keep test files under `tests/` and reusable logic under these root-level directories.

---

## Prerequisites & Installation

### 1. Initialize Your Environment

Make sure you have `uv` installed. If you don't, fetch it via `curl -LsSf https://astral.sh/uv/install.sh` or your system package manager. Then, install dependencies and set up code style validation hooks:

```bash
# Sync package specifications out of pyproject.toml
uv sync

# Install native Playwright system browser binaries
uv run playwright install --with-deps

# Bind local pre-commit hooks to your git lifecycle hooks context
uv run pre-commit install

```

### 2. Environment Configurations Setup

The framework leverages automated `.env` loading. Create your local context tracking files before launching scripts:

```bash
cp .env.example .env

```

Open your newly created `.env` file and customize your workspace targets securely:

```ini
BASE_URL=https://playwright.dev/
ADMIN_USER=your_private_username
ADMIN_PASSWORD=your_private_password

```

### 3. (Optional) Allure 3 Dashboard Engine

To spin up interactive Allure reporting, your host machine requires the Allure command-line utility binary. [https://allurereport.org/docs/v3/install/](https://allurereport.org/docs/v3/install/)

```bash
npm install -g allure

```

---

## Run Tests & Generate Reports

The suite is designed to change its reporting layout dynamically depending on the execution parameters passed down through the terminal command:

### Choice A: Generate Lightweight Pytest-HTML Reports

Creates a self-contained, lightweight `.html` build artifact file inside a custom `reports/` directory with embedded links to failure videos.

```bash
uv run pytest --html=true --self-contained-html

```

### Choice B: Generate Advanced Allure 3 Interactive Dashboards

Compiles a graphical dashboard detailing timelines, error trace breakdowns, nested failures, expandable screenshots, and interactive inline streaming `.webm` videos.

```bash
# 1. Run the test suite to harvest raw metadata
uv run pytest --alluredir=allure-results

# 2. Compile metrics and launch a localized browser viewer server
allure serve allure-results

```

---

## Cross-Browser Testing

The framework supports Chromium, Firefox, and WebKit via the `--browser` flag. By default, pytest-playwright runs tests on Chromium.

### Run on Specific Browser

```bash
# Run tests on Chromium (default)
uv run pytest --browser chromium

# Run tests on Firefox
uv run pytest --browser firefox

# Run tests on WebKit (Safari engine)
uv run pytest --browser webkit
```

### Run on All Browsers

```bash
# Execute tests sequentially across all browsers
uv run pytest --browser chromium --browser firefox --browser webkit
```

### Device Emulation

```bash
# Run tests emulating a specific device
uv run pytest --device "iPhone 13"
uv run pytest --device "Pixel 5"
```

### Headed Mode

```bash
# Run with visible browser window for debugging
uv run pytest --headed --browser chromium
```

---

## Useful Pytest Command Line Flags

When executing `uv run pytest`, you can append these optional flags to control output verbosity, parallel execution, or debugging parameters:

### 1. Visual Debugging & Local Execution Controls
* `--headed`: **Disables headless mode.** Launches a physical, visible browser window on your monitor so you can watch the test execution, clicks, and transitions happen live.
* `--slowmo <ms>`: **Introduces action delays.** Slows down all automated browser actions (clicks, inputs, navigations) by a set duration in milliseconds. Great for tracing fast visual flows (e.g., `uv run pytest --headed --slowmo 500`).
* `--devtools`: **Launches browser developer tools.** Automatically spins up a headed browser window with the Chrome/Firefox Inspector console pre-docked. Perfect for profiling network payloads or tracking DOM selectors mid-test.

### 2. Output & Logging Controls

* `-s` (or `--capture=no`): **Disables output capturing.** Forces Pytest to print all standard out logs (`print()` statements) immediately to the console. Use this if you are missing your Setup or Teardown messages.
* `-v`: **Verbose mode.** Displays the full name of every individual test and its parametrization parameters instead of just dots (`.F`).
* `-rA`: **Show All Output.** Forces Pytest to print a comprehensive summary at the end of the run containing the captured `stdout`/`stderr` text blocks for *both* passed and failed tests.

### 3. Execution Control & Diagnostics

* `-x` (or `--exitfirst`): **Stop on first failure.** Instantly terminates the entire test suite run the moment a single test fails. Ideal for debugging continuous integration pipelines.
* `--lf` (or `--last-failed`): **Run only failures.** Reads the cache memory and re-runs only the specific tests that failed during the previous execution session.
* `-k "expression"`: **Filter by test name.** Runs tests whose names match a keyword filter string (e.g., `uv run pytest -k "login"` runs only login-related tests).

### 4. Parallelization & Scaling

* `-n <num>`: **Multi-threaded execution** (via `pytest-xdist`). Spreads tests concurrently across multiple local machine CPU worker cores:

```bash
# Automatically scale threads across all available CPU cores
uv run pytest -n auto

```

*(If your terminal context experiences Java environment limitations, serve explicitly via Node: `npx allure-commandline serve allure-results`)*

---

## Configuration Details (`pytest.ini`)

Global default parameters reside directly inside `pytest.ini` to enforce strict marker definitions, setup logging rules, and dictate default browser video retention logic:

```ini
[pytest]
pythonpath = .
testpaths = tests
addopts = -ra --strict-markers --tb=short --color=yes --video retain-on-failure

# Strict Custom Markers Configuration
markers =
    api: API path tests.
    smoke: Critical core regression path tests.
    regression: Comprehensive full system checks.
    ui: Frontend visual browser verification tests.

# Live Console Streaming Logs Configuration
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)
log_cli_date_format = %Y-%m-%d %H:%M:%S

reruns = 2
reruns_delay = 1

```

*Note: `--video retain-on-failure` guarantees videos are safely discarded for passing tests, preserving local storage.*

---

## Git Best Practices & Untracked Files

The following local runtime artifacts, secrets, and environment managers generated during execution must remain completely untracked. Ensure your local `.gitignore` configuration matches the framework blueprint:

```text
.env
*.env
test-results/
allure-results/
allure-report/
reports/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.venv/
node_modules/

```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
