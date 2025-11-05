"""
constants/Dsystemd.py

    systemctl - A Python wrapper for the systemctl command line utility.
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/systemctl
    License: GPL 3.0
"""

from typing import TypedDict, Final

TIMEOUT_MSG = "systemctl timed out"
SYSTEMCTL = "systemctl"
SUDO = "sudo"
TIMEOUT = 10


class _DSystemd(TypedDict):
    ENABLE: str
    DISABLE: str
    RESTART: str
    STATUS: str
    START: str
    STOP: str


class DSystemd:
    ENABLE: Final[str] = "enable"
    DISABLE: Final[str] = "disable"
    RESTART: Final[str] = "restart"
    STATUS: Final[str] = "status"
    START: Final[str] = "start"
    STOP: Final[str] = "stop"

    ALL: Final[_DSystemd] = {
        "ENABLE": ENABLE,
        "DISABLE": DISABLE,
        "RESTART": RESTART,
        "STATUS": STATUS,
        "START": START,
        "STOP": STOP,
    }
