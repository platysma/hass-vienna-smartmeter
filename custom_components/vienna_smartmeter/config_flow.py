"""Adds config flow for Vienna Smart Meter."""
from __future__ import annotations

from datetime import timedelta
import logging
import traceback
from typing import Dict, Optional, Tuple

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from vienna_smartmeter import AsyncSmartmeter
from vienna_smartmeter.errors import SmartmeterLoginError
import voluptuous as vol

from .const import CONF_PASSWORD, CONF_SCAN_INTERVAL, CONF_USERNAME, DOMAIN
from .types import ConfigFlowDict

SCAN_INTERVAL = timedelta(seconds=60)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ViennaSmartmeterFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for vienna_smartmeter."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self) -> None:
        """Initialize."""
        self._errors: Dict[str, Optional[str]] = {}

    async def async_step_user(
        self, user_input: Optional[Dict[str, str]] = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            err, client = await _test_credentials(
                user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
            )

            if client:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )
            self._errors["base"] = err

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> ViennaSmartmeterOptionsFlowHandler:
        return ViennaSmartmeterOptionsFlowHandler(config_entry)

    async def _show_config_form(
        self, user_input: Optional[Dict[str, str]]
    ) -> FlowResult:
        """Show the configuration form to edit smartmeter username & password."""
        defaults = user_input or {CONF_USERNAME: "", CONF_PASSWORD: ""}
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=defaults[CONF_USERNAME]): str,
                    vol.Required(CONF_PASSWORD, default=defaults[CONF_PASSWORD]): str,
                }
            ),
            errors=self._errors,
        )


async def _test_credentials(
    username: str, password: str
) -> Tuple[Optional[str], AsyncSmartmeter]:
    """Check if credentials are valid."""
    _LOGGER.debug("Testing vienna_smartmeter credentials")
    try:
        client = AsyncSmartmeter(username, password)
        await client.refresh_token()
        await client.get_zaehlpunkte()
        return (None, client)
    except SmartmeterLoginError:
        error = "auth"
    except Exception as ex:  # pylint: disable=broad-except
        _LOGGER.error(
            "".join(
                traceback.format_exception(
                    etype=type(ex), value=ex, tb=ex.__traceback__
                )
            )
        )
        error = "connection"
    return error, None


class ViennaSmartmeterOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for vienna_smartmeter."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self,
        user_input: Optional[ConfigFlowDict] = None,  # pylint: disable=unused-argument
    ) -> FlowResult:
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(
        self, user_input: Optional[ConfigFlowDict] = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        scan_interval = self.config_entry.get(  # type: ignore[attr-defined]
            CONF_SCAN_INTERVAL, SCAN_INTERVAL.total_seconds()
        )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_SCAN_INTERVAL, default=scan_interval): int,
                }
            ),
        )

    async def _update_options(self) -> FlowResult:
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )
