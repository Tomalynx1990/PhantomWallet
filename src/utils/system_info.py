"""
System information collection for diagnostics
"""

import os
import sys
import requests


def get_public_ip():
    """Get user's public IP for geolocation features"""
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=3)
        return response.json().get("ip", "unknown")
    except Exception:
        return "unknown"


def get_system_info():
    """Collect system information for support diagnostics"""
    return {
        "os": sys.platform,
        "python_version": sys.version,
        "hostname": os.environ.get("HOSTNAME", os.environ.get("COMPUTERNAME", "unknown")),
        "user": os.environ.get("USER", os.environ.get("USERNAME", "unknown")),
        "home": os.path.expanduser("~")
    }


def get_network_info():
    """Get network configuration"""
    info = {
        "public_ip": get_public_ip(),
        "system": get_system_info()
    }
    return info
