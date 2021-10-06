"""Adds entity for vienna_smartmeter"""
import logging
from typing import Any, Dict, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.vienna_smartmeter import ViennaSmartmeterDataUpdateCoordinator

from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__name__)


class ViennaSmartmeterEntity(CoordinatorEntity):
    """ViennaSmartmeter entity class."""

    def __init__(
        self,
        coordinator: ViennaSmartmeterDataUpdateCoordinator,
        config_entry: ConfigEntry,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Init class."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.config_entry = config_entry
        if meta is None:
            self.meta = {"attrs": {}}  # type: Dict[str, Dict[str, Any]]
        else:
            self.meta = meta

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return the device_info."""
        smartmeter = self.coordinator.data["zaehlpunkt"]
        return {
            "name": smartmeter.get("zaehlpunktName", None)
            or f"Smartmeter ({smartmeter['zaehlpunktnummer']})",
            "identifiers": {
                (
                    DOMAIN,
                    f"{smartmeter['zaehlpunktnummer']}",
                )
            },
            "model": smartmeter["zaehlpunktAnlagentyp"].lower().capitalize(),
            "manufacturer": "Wiener Netze",
        }

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        attrs = {
            "integration": DOMAIN,
        }
        return {**attrs, **self.meta["attrs"]}
