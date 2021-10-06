"""
Custom integration to integrate Vienna Smart Meter with Home Assistant.

For more details about this integration, please refer to
https://github.com/platysma/hass-vienna-smartmeter
"""
import asyncio
from datetime import timedelta
import logging
from typing import Any, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from vienna_smartmeter._async.client import AsyncSmartmeter

from .const import (
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    client = AsyncSmartmeter(username, password, async_get_clientsession(hass))

    coordinator = ViennaSmartmeterDataUpdateCoordinator(
        hass, client=client, entry=entry
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        job = hass.config_entries.async_forward_entry_setup(entry, platform)
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(job)  # type: ignore[arg-type]

    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


class ViennaSmartmeterDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Vienna Smartmeter API."""

    def __init__(
        self, hass: HomeAssistant, client: AsyncSmartmeter, entry: ConfigEntry
    ) -> None:
        """Initialize."""
        self.client = client
        self.platforms: List[Any] = []

        scan_interval = timedelta(
            seconds=entry.options.get(
                CONF_SCAN_INTERVAL,
                entry.data.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL.total_seconds()),
            )
        )
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=scan_interval)

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            _LOGGER.debug("Refreshing Vienna Smartmeter update coordinator")
            await self.client.refresh_token()
            return await self.client.welcome()
        except Exception as exception:
            raise UpdateFailed() from exception
