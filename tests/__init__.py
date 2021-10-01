"""Tests for Vienna Smart Meter integration."""

from custom_components.vienna_smartmeter import config_flow, const

MOCK_DATA = {
    config_flow.CONF_USERNAME: const.CONF_USERNAME,
    config_flow.CONF_PASSWORD: const.CONF_PASSWORD,
}
