"""Various types used in type hints."""

from typing import TypedDict


class ConfigFlowDict(TypedDict):
    """Typed dict for config flow handler"""

    username: str
    password: str
