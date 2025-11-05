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

# Import systemctl constant definitions
from systemctl.constants.DEnviron import DEnviron
from systemctl.constants.DResult import DResult
from systemctl.constants.DSystemctl import (
    DSystemd,
    TIMEOUT_MSG,
    SYSTEMCTL,
    SUDO,
    TIMEOUT,
)


class systemctl:

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
        self.status()

    def active(self):
        """
        Return a boolean indicating if the service is running or not.
        """
        self.status()
        return self.result[DResult.ACTIVE]

    def disable(self):
        """
        Disable the service.
        """
        return self._run_systemctl(DSystemd.DISABLE)

    def enable(self):
        """
        Enable the service.
        """
        return self._run_systemctl(DSystemd.ENABLE)

    def enabled(self):
        """
        Return a boolean indicating if a service is enabled or not.
        """
        return self.result[DResult.ENABLED]

    def installed(self):
        """
        Return a boolean indicating if the service is present at all.
        """
        if self.stderr():
            return False
        return True

    def pid(self):
        """
        Return the PID of a running service.
        """
        return self.result[DResult.PID]

    def restart(self):
        """
        Restart a service.
        """
        return self._run_systemctl(DSystemd.RESTART)

    def service_name(self, service_name=None):
        """
        Get/Set the service_name.
        """
        old_service_name = self._service_name
        if service_name:
            self._service_name = service_name
            if service_name != old_service_name:
                self.status()
        return self._service_name

    def start(self):
        """
        Start a systemd service.
        """
        return self._run_systemctl(DSystemd.START)

    def status(self):
        """
        (Re)load the instance's result's dictionary.
        """

        self._run_systemctl(DSystemd.STATUS)
        stdout = self.stdout()
        stderr = self.stderr()

        if "could not be found" in stderr:
            return

        # print(f"Db4ESystemD:status(): stdout: {stdout}")
        # Check for active state
        if re.search(r"^\s*Active:\s+active \(running\).*", stdout, re.MULTILINE):
            self.result[DResult.ACTIVE] = True
        elif re.search(r"^\s*Active:\s+inactive \(dead\).*", stdout, re.MULTILINE):
            self.result[DResult.ACTIVE] = False
        elif re.search(r"^\s*Active:\s+failed.*", stdout, re.MULTILINE):
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
        return self._run_systemctl(DSystemd.STOP)

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
        if arg == DSystemd.STATUS:
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
            self.result[DResult.RAW_STDOUT] = TIMEOUT_MSG
            return 5

        except Exception as e:
            self.result[DResult.RAW_STDERR] = str(e)
            return 5

        self.result[DResult.RAW_STDOUT] = stdout
        self.result[DResult.RAW_STDERR] = stderr

        if arg == DSystemd.ENABLE or arg == DSystemd.DISABLE:
            # Reload the status information
            self.status()

        # Return the return code for the systemctl command
        return proc.returncode
