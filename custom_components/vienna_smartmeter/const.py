"""Constants for Vienna Smartmeter."""
# Base component constants
NAME = "Vienna Smartmeter"
DOMAIN = "vienna_smartmeter"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.1.0"

ATTRIBUTION = "Data provided by https://www.wienernetze.at/smartmeter"
ISSUE_URL = "https://github.com/platysma/hass-vienna-smartmeter/issues"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

DEFAULT_USERNAME = "demouser"
DEFAULT_PASSWORD = "Demouser123"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
A custom, unofficial integration to access the Vienna Smartmeter API.
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
