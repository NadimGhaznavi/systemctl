# constants/DSystemctl.py
#
#    systemctl - A Python wrapper for the systemctl command line utility.
#    Author: Nadim-Daniel Ghaznavi
#    Copyright: (c) 2025 Nadim-Daniel Ghaznavi
#    GitHub: https://github.com/NadimGhaznavi/systemctl
#    License: GPL 3.0


class DSystemCtl:
    """Constants related to systemctl commands."""

    ENABLE: str = "enable"
    DISABLE: str = "disable"
    RESTART: str = "restart"
    STATUS: str = "status"
    START: str = "start"
    STOP: str = "stop"
    TIMEOUT: int = 10
