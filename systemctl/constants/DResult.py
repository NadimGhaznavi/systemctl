"""
constants/DResult.py

    systemctl - A Python wrapper for the systemctl command line utility.
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/systemctl
    License: GPL 3.0
"""

from typing import TypedDict, Final


class _DResult(TypedDict):
    ACTIVE: str
    PID: str
    ENABLED: str
    RAW_STDOUT: str
    RAW_STDERR: str


class DResult:
    """Constants related to parsed systemctl command results."""

    ACTIVE: Final[str] = "active"
    PID: Final[str] = "pid"
    ENABLED: Final[str] = "enabled"
    RAW_STDOUT: Final[str] = "raw_stdout"
    RAW_STDERR: Final[str] = "raw_stderr"

    ALL: Final[_DResult] = {
        "ACTIVE": ACTIVE,
        "PID": PID,
        "ENABLED": ENABLED,
        "RAW_STDOUT": RAW_STDOUT,
        "RAW_STDERR": RAW_STDERR,
    }
