"""All smartmeter errors."""


class SmartmeterError(Exception):
    """The root of all Smartmeter madness."""


class SmartmeterLoginError(SmartmeterError):
    """Authentication failed."""
