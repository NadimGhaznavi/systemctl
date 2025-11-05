# constants/DResult.py
#
#    systemctl - A Python wrapper for the systemctl command line utility.
#   Author: Nadim-Daniel Ghaznavi
#    Copyright: (c) 2025 Nadim-Daniel Ghaznavi
#    GitHub: https://github.com/NadimGhaznavi/systemctl
#    License: GPL 3.0


class DResult:
    """Constants related to parsed systemctl command results."""

    ACTIVE: str = "active"
    PID: str = "pid"
    ENABLED: str = "enabled"
    RAW_STDOUT: str = "raw_stdout"
    RAW_STDERR: str = "raw_stderr"
