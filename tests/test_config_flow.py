from unittest.mock import patch

import pytest

from custom_components.vienna_smartmeter import const
from homeassistant import data_entry_flow

from . import MOCK_DATA


async def test_import(hass, api):
    """Test import step."""
    result = await hass.config_entries.flow.async_init(
        const.DOMAIN, context={"source": "import"}, data=MOCK_DATA
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "Mikrotik"
    assert result["data"][CONF_NAME] == "Mikrotik"
    assert result["data"][CONF_HOST] == "10.0.0.1"
    assert result["data"][CONF_USERNAME] == "admin"
    assert result["data"][CONF_PASSWORD] == "admin"
    assert result["data"][CONF_PORT] == 0
    assert result["data"][CONF_SSL] is False
