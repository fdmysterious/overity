"""
Utilities to dump environment information
=========================================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""


def platform_info():
    import platform

    uname_info = platform.uname()

    return {
        "hostname": uname_info.node,
        "machine": uname_info.machine,
        "os_system": uname_info.system,
        "os_release": uname_info.release,
        "os_version": uname_info.version,
    }


def installed_packages():
    """List installed packages in current environment using pip freeze"""
    import subprocess

    output = subprocess.run(["pip", "freeze"], capture_output=True)

    # Parse output
    pkg_list = output.stdout.decode("utf-8").split("\n")

    return pkg_list
