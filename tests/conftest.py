"""Global fixtures for vienna_smartmeter integration."""
# Fixtures allow you to replace functions with a Mock object. You can perform
# many options via the Mock to reflect a particular behavior from the original
# function that you want to see without going through the function's actual logic.
# Fixtures can either be passed into tests as parameters, or if autouse=True, they
# will automatically be used across all tests.
#
# Fixtures that are defined in conftest.py are available across all tests. You can also
# define fixtures within a particular test file to scope them locally.
#
# pytest_homeassistant_custom_component provides some fixtures that are provided by
# Home Assistant core.
#
# See here for more info: https://docs.pytest.org/en/latest/fixture.html (note that
# pytest includes fixtures OOB which you can use as defined on this page)
from unittest.mock import patch

import pytest
from vienna_smartmeter.errors import SmartmeterLoginError

from tests import load_fixture_json

pytest_plugins = "pytest_homeassistant_custom_component"  # pylint: disable=invalid-name


# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Auto enable custom integrations."""
    yield


# This fixture is used to prevent HomeAssistant from attempting to create
# and dismiss persistent notifications. These calls would fail without this
# fixture since the persistent_notification integration is never
# loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


# This fixture, when used, will result in calls to async_get_data to return None.
# To have the call return a value, we would add the
# `return_value=<VALUE_TO_RETURN>` parameter to the patch call.
@pytest.fixture(name="bypass_get_data")
def bypass_get_data_fixture():
    """Skip calls to get data from API."""
    with patch(
        "vienna_smartmeter.AsyncSmartmeter.welcome",
        return_value=load_fixture_json("welcome_data"),
    ):
        yield


# In this fixture, we are forcing calls to async_get_data to raise an Exception.
# This is useful for exception handling.
@pytest.fixture(name="error_on_get_data")
def error_get_data_fixture():
    """Simulate error when retrieving data from API."""
    with patch(
        "vienna_smartmeter.AsyncSmartmeter.welcome",
        side_effect=Exception,
    ):
        yield


# In this fixture, we are forcing calls to async_get_data to
# raise an Exception. This is useful for exception handling.
@pytest.fixture(name="auth_error_on_get_data")
def auth_error_get_data_fixture():
    """Simulate authentication error when retrieving data from API."""
    with patch(
        "vienna_smartmeter.AsyncSmartmeter.welcome",
        side_effect=SmartmeterLoginError,
    ):
        yield


# In this fixture, we are forcing calls to async_get_data
# to raise an Exception. This is useful for exception handling.
@pytest.fixture(name="timeout_error_on_get_data")
def timeout_error_get_data_fixture():
    """Simulate Timeout error when retrieving data from API."""
    with patch(
        "vienna_smartmeter._async.client.AsyncSmartmeter._request",
        side_effect=Exception,
    ), patch(
        "vienna_smartmeter.AsyncSmartmeter._request",
        side_effect=Exception,
    ):
        yield
