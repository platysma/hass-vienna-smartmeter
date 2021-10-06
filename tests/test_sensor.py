"""Test vienna_smartmeter sensor."""

from homeassistant.core import HomeAssistant

from . import setup_mock_smartmeter_config_entry

TEST_HUB_SENSOR_POWER_GRID_ENTITY_ID = "sensor.myenergi_test_site_power_grid"
TEST_SENSOR_METER_ENTITY_ID = "sensor.meter_reading"  # sensor.meter_reading
TEST_SENSOR_METER_YESTERDAY_ENTITY_ID = (
    "sensor.consumption_yesterday"  # sensor.consumption_yesterday
)
TEST_SENSOR_METER_DAYBEFOREYESTERDAY_ENTITY_ID = (
    "sensor.consumption_day_before_yesterday"  # sensor.consumption_day_before_yesterday
)


async def test_meter_sensor(hass: HomeAssistant) -> None:
    """Verify device information includes expected details."""

    await setup_mock_smartmeter_config_entry(hass)

    entity_state = hass.states.get(TEST_SENSOR_METER_ENTITY_ID)
    assert entity_state
    assert entity_state.state == "20857.619"


async def test_meter_yesterday_sensor(hass: HomeAssistant) -> None:
    """Verify device information includes expected details."""

    await setup_mock_smartmeter_config_entry(hass)

    entity_state = hass.states.get(TEST_SENSOR_METER_YESTERDAY_ENTITY_ID)
    assert entity_state
    assert entity_state.state == "9.509"


async def test_meter_day_before_yesterday_sensor(hass: HomeAssistant) -> None:
    """Verify device information includes expected details."""

    await setup_mock_smartmeter_config_entry(hass)

    entity_state = hass.states.get(TEST_SENSOR_METER_DAYBEFOREYESTERDAY_ENTITY_ID)
    assert entity_state
    assert entity_state.state == "7.583"
