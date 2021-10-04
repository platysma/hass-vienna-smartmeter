"""Adds config flow for Vienna Smart Meter."""
from __future__ import annotations

import logging
from typing import Dict, Optional

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from vienna_smartmeter import AsyncSmartmeter
import voluptuous as vol

from .const import CONF_PASSWORD, CONF_USERNAME, DOMAIN, PLATFORMS
from .types import ConfigFlowDict

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ViennaSmartmeterFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for vienna_smartmeter."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self) -> None:
        """Initialize."""
        self._errors: Dict[str, str] = {}

    async def async_step_user(
        self, user_input: Optional[Dict[str, str]] = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            valid = await _test_credentials(
                user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
            )

            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )
            self._errors["base"] = "auth"

            return await self._show_config_form()

        return await self._show_config_form()

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> ViennaSmartmeterOptionsFlowHandler:
        return ViennaSmartmeterOptionsFlowHandler(config_entry)

    async def _show_config_form(self) -> FlowResult:
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}
            ),
            errors=self._errors,
        )


async def _test_credentials(username: str, password: str) -> bool:
    """Return true if credentials is valid."""
    try:
        client = AsyncSmartmeter(username, password)
        await client.refresh_token()
        await client.get_zaehlpunkte()
        return True
    except Exception as exception:  # pylint: disable=broad-except
        _LOGGER.exception(exception)
    return False


class ViennaSmartmeterOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for vienna_smartmeter."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: Optional[ConfigFlowDict] = None
    ) -> FlowResult:
        """Manage the options."""
        return await self.async_step_user(user_input)

    async def async_step_user(
        self, user_input: Optional[ConfigFlowDict] = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self) -> FlowResult:
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )
