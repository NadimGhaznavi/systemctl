"""
constants/DSystemctl.py

    systemctl - A Python wrapper for the systemctl command line utility.
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/systemctl
    License: GPL 3.0
"""

from typing import TypedDict, Final

SYSTEMCTL = "systemctl"
SUDO = "sudo"
TIMEOUT = 10


class _DSystemCtl(TypedDict):
    ENABLE: str
    DISABLE: str
    RESTART: str
    STATUS: str
    START: str
    STOP: str


class DSystemCtl:
    """Constants related to systemctl commands."""

    ENABLE: Final[str] = "enable"
    DISABLE: Final[str] = "disable"
    RESTART: Final[str] = "restart"
    STATUS: Final[str] = "status"
    START: Final[str] = "start"
    STOP: Final[str] = "stop"

    ALL: Final[_DSystemCtl] = {
        "ENABLE": ENABLE,
        "DISABLE": DISABLE,
        "RESTART": RESTART,
        "STATUS": STATUS,
        "START": START,
        "STOP": STOP,
    }


class _DMsg(TypedDict):
    NO_SERVICE_NAME: str
    NOT_FOUND: str
    TIMEOUT: str


class DMsg:
    """Constants related to systemctl messages."""

    NO_SERVICE_NAME: Final[str] = "service name not specified"
    NOT_FOUND: Final[str] = "could not be found"
    TIMEOUT: Final[str] = "systemctl timed out"

    ALL: Final[_DMsg] = {
        "NO_SERVICE_NAME": NO_SERVICE_NAME,
        "NOT_FOUND": NOT_FOUND,
        "TIMEOUT": TIMEOUT,
    }
