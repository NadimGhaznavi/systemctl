"""
systemctl/__init__.py

    systemctl - A Python wrapper for the systemctl command line utility.
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/systemctl
    License: GPL 3.0
"""

# Import supporting modules
import os
import subprocess
import re
from enum import IntEnum

# Import systemctl constant definitions
from systemctl.constants.DEnviron import DEnviron
from systemctl.constants.DResult import DResult
from systemctl.constants.DSystemCtl import DSystemCtl as DSystemCtl
from systemctl.constants.DSystemCtl import DMsg as DMsg
from systemctl.constants.DSystemCtl import (
    SYSTEMCTL,
    SUDO,
    TIMEOUT,
)


class ExitCode(IntEnum):
    OK = 0
    ERROR = 5


class SystemCtl:

    def __init__(self, service_name=None):
        # Make sure systemd doesn't clutter the output with color codes or use a pager
        os.environ[DEnviron.SYSTEMD_COLORS] = "0"
        os.environ[DEnviron.SYSTEMD_PAGER] = ""
        self.result = {
            DResult.ACTIVE: None,
            DResult.PID: None,
            DResult.ENABLED: None,
            DResult.RAW_STDOUT: "",
            DResult.RAW_STDERR: "",
        }
        self._service_name = service_name
        self._timeout = TIMEOUT
        self._update_status()

    def disable(self):
        """
        Disable the service.
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)
        return self._run_systemctl(DSystemCtl.DISABLE)

    def enable(self):
        """
        Enable the service.
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)
        return self._run_systemctl(DSystemCtl.ENABLE)

    def enabled(self):
        """
        Return a boolean indicating if a service is enabled or not.
        """
        return self.result[DResult.ENABLED]

    def installed(self):
        """
        Return a boolean indicating if the service is present at all.
        """
        return not self.stderr()

    def pid(self):
        """
        Return the PID of a running service.
        """
        return self.result[DResult.PID]

    def restart(self):
        """
        Restart a service.
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)
        return self._run_systemctl(DSystemCtl.RESTART)

    def running(self):
        """
        Return a boolean indicating if the service is running or not.
        """
        self._update_status()
        return self.result[DResult.ACTIVE]

    def service_name(self, service_name=None):
        """
        Get/Set the service_name.
        """
        old_service_name = self._service_name
        if service_name:
            self._service_name = service_name
            if service_name != old_service_name:
                self._update_status()
        return self._service_name

    def start(self):
        """
        Start a systemd service.
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)
        return self._run_systemctl(DSystemCtl.START)

    def _update_status(self):
        """
        (Re)load the instance's result's dictionary.
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)

        self._run_systemctl(DSystemCtl.STATUS)
        stdout = self.stdout()
        stderr = self.stderr()

        if DMsg.NOT_FOUND in stderr:
            self.result[DResult.ACTIVE] = None
            self.result[DResult.PID] = None
            self.result[DResult.ENABLED] = None
            return

        # Check for active state
        if re.search(r"^\s*Active:\s+active \(running\).*", stdout, re.MULTILINE):
            self.result[DResult.ACTIVE] = True
        elif re.search(r"^\s*Main PID:.*\(code=exited\).*", stdout, re.MULTILINE):
            self.result[DResult.ACTIVE] = False
        elif re.search(r"^\s*Active:\s+inactive \(dead\).*", stdout, re.MULTILINE):
            self.result[DResult.ACTIVE] = False

        # Check for enabled state
        if re.search(r"Loaded: .*; enabled;", stdout):
            self.result[DResult.ENABLED] = True
        elif re.search(r"Loaded: .*; disabled;", stdout):
            self.result[DResult.ENABLED] = False

        # Get PID
        pid_match = re.search(r"^\s*Main PID:\s+(\d+)", stdout, re.MULTILINE)
        if pid_match and self.result[DResult.ACTIVE]:
            self.result[DResult.PID] = int(pid_match.group(1))

    def stdout(self):
        """
        Return the raw STDOUT of a 'systemctl status service_name' command.
        """
        return self.result[DResult.RAW_STDOUT]

    def stderr(self):
        """
        Return the raw STDERR of a 'systemctl status service_name' command.
        """
        return self.result[DResult.RAW_STDERR]

    def stop(self):
        """
        Stop a systemd service.
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)
        return self._run_systemctl(DSystemCtl.STOP)

    def timeout(self, timeout=None):
        """
        Get/Set the timeout.
        """
        if timeout is not None:
            self._timeout = timeout
        return self._timeout

    def _run_systemctl(self, arg):
        """
        Execute a 'systemctl [start|stop|restart|status|enable|disable] service_name'
        command and load the instance's result dictionary.
        """
        if arg == DSystemCtl.STATUS:
            cmd = [SYSTEMCTL, arg, self._service_name]
        else:
            cmd = [SUDO, SYSTEMCTL, arg, self._service_name]

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                input="",
                timeout=self._timeout,
            )
            stdout = proc.stdout.decode(errors="replace")
            stderr = proc.stderr.decode(errors="replace")

        except subprocess.TimeoutExpired:
            self.result[DResult.RAW_STDOUT] = ""
            self.result[DResult.RAW_STDERR] = DMsg.TIMEOUT
            return ExitCode.ERROR

        except Exception as e:
            self.result[DResult.RAW_STDOUT] = ""
            self.result[DResult.RAW_STDERR] = str(e)
            return ExitCode.ERROR

        self.result[DResult.RAW_STDOUT] = stdout
        self.result[DResult.RAW_STDERR] = stderr

        if arg == DSystemCtl.ENABLE or arg == DSystemCtl.DISABLE:
            # Reload the status information
            self._update_status()

        # Return the return code for the systemctl command
        return proc.returncode
