---
title: systemctl
layout: default
---
# Introduction

A lightweight Python wrapper for the `systemctl` command, designed for use in Python-based service managers, admin tools, and dashboards.

---

# Features

* Query service status, PID, and enable status
* Start, stop, and restart services
* Enable and disable services
* Structured output, clean API
* Parses and interprets `systemctl` output

**IMPORTANT NOTE:** All `systemctl` operations except for `sysemctl status` require root access. This module uses `sudo` to deal with this fact. It's recommended that you use a fine-grained sudo configuration. For example, the following two lines in the `/etc/sudoers` file allow the *sally* user to start and stop the *db4e* services **without prompting for a password** to make your Python project run smoothly.

```
sally ALL=(ALL) NOPASSWD: /bin/systemctl start db4e
sally ALL=(ALL) NOPASSWD: /bin/systemctl stop db4e
```

The above *sudo configuration* script that *sally* runs that uses this module will be successful in starting and stopping the *db4e* service, but will fail if `enable()` or `disable()` are attempted.

---

# Installation

```bash
pip install systemctl
```

Or clone locally:

```bash
git clone https://github.com/NadimGhaznavi/systemctl
```

---

# Example Usage

```python
from systemctl.systemctl import systemctl

svc = systemctl('db4e')

if not svc.installed():
    print("Service not installed")
elif not svc.active():
    print("Service is stopped. Starting...")
    svc.start()
else:
    print(f"Service is running with PID {svc.pid()}")
```

---

# Methods

```python
svc = Db4eSystemd('myservice')

svc.start()          # Start service
svc.stop()           # Stop service
svc.restart()        # Restart service
svc.enable()         # Enable service startup at boot time
svc.disable()        # Disable service startup at boot time
svc.status()         # Refresh status
svc.active()         # True/False
svc.enabled()        # True/False
svc.installed()      # True/False
svc.pid()            # Integer PID or None
svc.stdout()         # Raw systemctl stdout
svc.stderr()         # Raw systemctl stderr
```

---

# License

GPL v3 - See LICENSE.txt

---

Created and maintained by Nadim-Daniel Ghaznavi. This module was developed as a component for the [Database 4 Everything](https://db4e.osoyalce.com) project.

