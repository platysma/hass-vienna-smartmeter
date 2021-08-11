class SmartmeterError(Exception):
    """The root of all Smartmeter madness."""

    pass


class SmartmeterLoginError(SmartmeterError):
    """Authentication failed."""

    pass
