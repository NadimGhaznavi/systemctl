# systemctl/__init__.py
#
#    systemctl - A Python wrapper for the systemctl command line utility.
#    Author: Nadim-Daniel Ghaznavi
#    Copyright: (c) 2025 Nadim-Daniel Ghaznavi
#    GitHub: https://github.com/NadimGhaznavi/systemctl
#    License: GPL 3.0

# Import supporting modules
import os
import subprocess
import re
from enum import IntEnum

# Import systemctl constant definitions
from systemctl.constants.DCmd import DCmd
from systemctl.constants.DEnviron import DEnviron
from systemctl.constants.DExitCode import DExitCode
from systemctl.constants.DMsg import DMsg
from systemctl.constants.DResult import DResult
from systemctl.constants.DSystemCtl import DSystemCtl


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
        self._timeout = DSystemCtl.TIMEOUT
        self._update_status()

    def start(self):
        """
        Start a systemd service.

        :return: The exit code of the systemctl command.
        :rtype: int
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)
        return self._run_systemctl(DSystemCtl.START)

    def stop(self):
        """
        Stop a systemd service.

        :return: The exit code of the systemctl command.
        :rtype: int
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)
        return self._run_systemctl(DSystemCtl.STOP)

    def restart(self):
        """
        Restart a service.

        :return: The exit code of the systemctl command.
        :rtype: int
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)
        return self._run_systemctl(DSystemCtl.RESTART)

    def enable(self):
        """
        Enable the service.

        :return: The exit code of the systemctl command.
        :rtype: int
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)
        return self._run_systemctl(DSystemCtl.ENABLE)

    def disable(self):
        """
        Disable the service.

        :return: The exit code of the systemctl command.
        :rtype: int
        """
        if not self._service_name:
            raise ValueError(DMsg.NO_SERVICE_NAME)
        return self._run_systemctl(DSystemCtl.DISABLE)

    def service_name(self, service_name=None):
        """
        Get/Set the service_name.

        :param: Optional service name.
        :type: str
        :return: The service name.
        :rtype: str
        """
        old_service_name = self._service_name
        if service_name:
            self._service_name = service_name
            if service_name != old_service_name:
                self._update_status()
        return self._service_name

    def enabled(self):
        """
        :return: Whether or not the service is enabled.
        :rtype: bool
        """
        return self.result[DResult.ENABLED]

    def installed(self):
        """
        :return: Whether the service is present at all.
        :rtype: bool
        """
        return not self.stderr()

    def running(self):
        """
        :return: Whether or not the service is running.
        :rtype: bool
        """
        self._update_status()
        return self.result[DResult.ACTIVE]

    def pid(self):
        """
        :return: The PID of the running service.
        :rtype: int
        """
        return self.result[DResult.PID]

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
        :return: The raw STDOUT of a 'systemctl status service_name' command.
        :rtype: str
        """
        return self.result[DResult.RAW_STDOUT]

    def stderr(self):
        """
        :return: The raw STDERR of a 'systemctl status service_name' command.
        :rtype: str
        """
        return self.result[DResult.RAW_STDERR]

    def timeout(self, timeout=None):
        """
        :param: Optional timeout value for the systemctl command.
        :type: int
        :return: The timeout value.
        :rtype: int
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
            cmd = [DCmd.SYSTEMCTL, arg, self._service_name]
        else:
            cmd = [DCmd.SUDO, DCmd.SYSTEMCTL, arg, self._service_name]

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
            return DExitCode.ERROR

        except Exception as e:
            self.result[DResult.RAW_STDOUT] = ""
            self.result[DResult.RAW_STDERR] = str(e)
            return DExitCode.ERROR

        self.result[DResult.RAW_STDOUT] = stdout
        self.result[DResult.RAW_STDERR] = stderr

        if arg == DSystemCtl.ENABLE or arg == DSystemCtl.DISABLE:
            # Reload the status information
            self._update_status()

        # Return the return code for the systemctl command
        return proc.returncode
