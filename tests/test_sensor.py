"""Tests for the sensor module."""
from pytest_homeassistant_custom_component.async_mock import AsyncMock, MagicMock
from vienna_smartmeter.errors import SmartmeterLoginError

from custom_components.vienna_smartmeter.sensor import ViennaSmartmeterEntity


async def test_async_update_failed():
    """Tests a failed async_update."""
    api = MagicMock()
    api.getitem = AsyncMock(side_effect=SmartmeterLoginError)

    sensor = ViennaSmartmeterEntity(api)
    await sensor.async_update()

    assert sensor.available is False
