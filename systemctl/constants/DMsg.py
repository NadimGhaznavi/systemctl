# constants/DSystemctl.py
#
#    systemctl - A Python wrapper for the systemctl command line utility.
#    Author: Nadim-Daniel Ghaznavi
#    Copyright: (c) 2025 Nadim-Daniel Ghaznavi
#    GitHub: https://github.com/NadimGhaznavi/systemctl
#    License: GPL 3.0


class DMsg:
    """Constants related to systemctl messages."""

    NO_SERVICE_NAME: str = "service name not specified"
    NOT_FOUND: str = "could not be found"
    TIMEOUT: str = "systemctl timed out"
