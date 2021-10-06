"""Constants for smartmeter integration tests."""
from custom_components.vienna_smartmeter import const

MOCK_CONFIG = {
    const.CONF_USERNAME: const.DEFAULT_USERNAME,
    const.CONF_PASSWORD: const.DEFAULT_PASSWORD,
}

MOCK_FAIL_CONFIG = {
    const.CONF_USERNAME: "wrong_user",
    const.CONF_PASSWORD: "wrong_pass",
}
