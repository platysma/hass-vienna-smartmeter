"""Sensor platform for Vienna Smart Meter."""
import logging
from typing import Optional

from vienna_smartmeter import AsyncSmartmeter
from vienna_smartmeter.errors import SmartmeterLoginError

from homeassistant import config_entries, core
from homeassistant.const import ENERGY_WATT_HOUR
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, HomeAssistantType

from .const import CONF_PASSWORD, CONF_USERNAME, DEFAULT_NAME, DOMAIN, ICON, SENSOR

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    # Update our config to include new repos and remove those that have been removed.
    if config_entry.options:
        config.update(config_entry.options)
    session = async_get_clientsession(hass)
    # _LOGGER.info(config[CONF_USERNAME])
    client = AsyncSmartmeter(config[CONF_USERNAME], config[CONF_PASSWORD], session)
    # zaehlpunkte = await client.get_zaehlpunkte()
    # _LOGGER.info(zaehlpunkte)
    # meter_id = zaehlpunkte[0]["zaehlpunkte"][0]["zaehlpunktnummer"]
    async_add_entities([ViennaSmartmeterEntity(client)], update_before_add=True)


async def async_setup_platform(
    hass: HomeAssistantType, config: ConfigType, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""
    session = async_get_clientsession(hass)
    client = AsyncSmartmeter(config[CONF_USERNAME], config[CONF_PASSWORD], session)
    async_add_entities([ViennaSmartmeterEntity(client)], update_before_add=True)


class ViennaSmartmeterEntity(Entity):
    """Representation of a Vienna Smartmeter Sensor entity."""

    def __init__(self, api_client: AsyncSmartmeter):
        super().__init__()
        self.api_client = api_client
        self.meter_id = DEFAULT_NAME
        self._available = True
        self._state = None

    @property
    def unique_id(self) -> str:
        """Return a unique ID of the entity."""
        return self.meter_id

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return ENERGY_WATT_HOUR

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return ICON

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def state(self) -> Optional[str]:
        """Return the state of the sensor."""
        return self._state if self.state else None

    @property
    def device_class(self) -> str:
        """Return the device class of the sensor."""
        return "vienna_smartmeter__custom_device_class"
        # return DEVICE_CLASS_ENERGY

    async def async_update(self) -> None:
        """Update meter reading by accessing the api."""
        try:
            await self.api_client.refresh_token()
            api_data = await self.api_client.welcome()
            meter_data = api_data["zaehlpunkt"]["meterReadings"][0]["value"]

            self._state = meter_data
            self._available = True
        except SmartmeterLoginError:
            _LOGGER.exception("Smartmeter login failed for sensor %s", self.name)
            self._available = False
