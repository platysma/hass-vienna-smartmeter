"""Sensor platform for Vienna Smart Meter."""
from typing import Any, Dict, Optional, Union

from homeassistant import config_entries, core
from homeassistant.components.sensor import STATE_CLASS_TOTAL, SensorEntity
from homeassistant.const import DEVICE_CLASS_ENERGY, ENERGY_KILO_WATT_HOUR
from homeassistant.exceptions import InvalidStateError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.vienna_smartmeter import ViennaSmartmeterDataUpdateCoordinator
from custom_components.vienna_smartmeter.entity import ViennaSmartmeterEntity

from .const import DOMAIN


def create_energy_meta(
    name: str, keyword: str, state: Optional[str] = None
) -> Dict[str, Any]:
    """Create metadata dict for energy sensors."""
    return {
        "name": name,
        "keyword": keyword,
        "device_class": DEVICE_CLASS_ENERGY,
        "unit": ENERGY_KILO_WATT_HOUR,
        "icon": "mdi:flash",
        "state_class": state,
        "attrs": {},
    }


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    sensors = []

    sensors.append(
        ViennaSmartmeterSensor(
            coordinator,
            config_entry,
            create_energy_meta("Meter Reading", "meterReadings", STATE_CLASS_TOTAL),
        )
    )

    sensors.append(
        ViennaSmartmeterSensor(
            coordinator,
            config_entry,
            create_energy_meta("Consumption Yesterday", "consumptionYesterday"),
        )
    )

    sensors.append(
        ViennaSmartmeterSensor(
            coordinator,
            config_entry,
            create_energy_meta(
                "Consumption Day before Yesterday", "consumptionDayBeforeYesterday"
            ),
        )
    )

    async_add_entities(sensors, update_before_add=True)


class ViennaSmartmeterSensor(ViennaSmartmeterEntity, SensorEntity):
    """Vienna Smartmeter sensor class."""

    def __init__(
        self,
        coordinator: ViennaSmartmeterDataUpdateCoordinator,
        config_entry: config_entries.ConfigEntry,
        meta: Optional[Dict[str, Union[str, Dict[Any, Any]]]],
    ) -> None:
        """Init class."""
        super().__init__(coordinator, config_entry, meta=meta)

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID to use for this entity."""
        entry_id = {self.config_entry.entry_id}
        meter_id = {self.coordinator.data["zaehlpunkt"]["zaehlpunktnummer"]}
        keyword = self.meta["keyword"]
        return f"{entry_id}-{meter_id}-{keyword}"

    @property
    def name(self) -> Optional[str]:
        """Return the name of the sensor."""
        return self.meta.get("name")  # type: ignore[return-value]

    @property
    def state(self) -> float:
        """Return the state of the sensor."""
        keyword = self.meta["keyword"]
        meter_dict = self.coordinator.data["zaehlpunkt"][keyword]
        if isinstance(meter_dict, list):
            return int(meter_dict[0]["value"]) / 1000
        if isinstance(meter_dict, dict):
            return int(meter_dict["value"]) / 1000
        raise InvalidStateError(
            f"Invalid state encountered for entity {self.meta['name']}."
        )

    @property
    def unit_of_measurement(self) -> Optional[str]:
        """Return the unit of measurement of the sensor."""
        return self.meta.get("unit")  # type: ignore[return-value]

    @property
    def icon(self) -> Optional[str]:
        """Return the icon of the sensor."""
        return self.meta.get("icon")  # type: ignore[return-value]

    @property
    def device_class(self) -> Optional[str]:
        """Return the device class of the sensor."""
        return self.meta.get("device_class")  # type: ignore[return-value]

    @property
    def state_class(self) -> Optional[str]:
        """Return the state class of the sensor."""
        return self.meta.get("state_class")  # type: ignore[return-value]
