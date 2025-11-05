"""
constants/DEnviron.py

    systemctl - A Python wrapper for the systemctl command line utility.
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/systemctl
    License: GPL 3.0
"""

from typing import TypedDict, Final


class _DEnviron(TypedDict):
    SYSTEMD_COLORS: str
    SYSTEMD_PAGER: str


class DEnviron:
    """Constants related to the runtime systemctl CLI environment."""

    SYSTEMD_COLORS: Final[str] = "SYSTEMD_COLORS"
    SYSTEMD_PAGER: Final[str] = "SYSTEMD_PAGER"

    ALL: Final[_DEnviron] = {
        "SYSTEMD_COLORS": SYSTEMD_COLORS,
        "SYSTEMD_PAGER": SYSTEMD_PAGER,
    }
