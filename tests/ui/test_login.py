import pytest

from pages.login_page import LoginPage


@pytest.mark.skip(reason="Template example - requires a real login page to run")
def test_invalid_login_triggers_error_banner(login_page: LoginPage):
    """Verify that invalid credentials display an error message."""
    login_page.navigate("/login")
    login_page.login("wrong_user", "bad_password")

    error_message = login_page.get_error_message_text()

    assert "Invalid credentials" in error_message
