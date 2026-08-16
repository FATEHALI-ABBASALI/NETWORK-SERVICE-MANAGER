"""
Application-wide constants.

This module contains fixed configuration used by the
Network Service Manager.

The application separates:

    1. Service ID
    2. Display name
    3. APT package name
    4. systemd service name

This is important because the Linux package name and
systemd service name are not always the same.
"""

# =========================================================
# Application
# =========================================================

APP_NAME = "Network Service Manager"
APP_VERSION = "1.0.0"

TARGET_PLATFORM = "Ubuntu Linux"


# =========================================================
# Service Identifiers
# =========================================================

SERVICE_SSH = "ssh"
SERVICE_FTP = "vsftpd"
SERVICE_NFS = "nfs-server"
SERVICE_SAMBA = "smbd"
SERVICE_APACHE = "apache2"
SERVICE_DNS = "bind9"
SERVICE_MYSQL = "mysql"


# =========================================================
# Service Display Names
# =========================================================

SERVICE_DISPLAY_NAMES = {
    SERVICE_SSH: "SSH / OpenSSH",
    SERVICE_FTP: "FTP",
    SERVICE_NFS: "NFS",
    SERVICE_SAMBA: "Samba",
    SERVICE_APACHE: "Apache",
    SERVICE_DNS: "DNS",
    SERVICE_MYSQL: "MySQL",
}


# =========================================================
# APT Package Names
# =========================================================
#
# These are the package names used by:
#
#     apt install <package>
#
# Example:
#
#     sudo apt install openssh-server
#
# =========================================================

SERVICE_PACKAGES = {
    SERVICE_SSH: "openssh-server",
    SERVICE_FTP: "vsftpd",
    SERVICE_NFS: "nfs-kernel-server",
    SERVICE_SAMBA: "samba",
    SERVICE_APACHE: "apache2",
    SERVICE_DNS: "bind9",
    SERVICE_MYSQL: "mysql-server",
}


# =========================================================
# systemd Service Names
# =========================================================
#
# These are the service names used by:
#
#     systemctl start <service>
#     systemctl stop <service>
#     systemctl restart <service>
#     systemctl enable <service>
#     systemctl disable <service>
#     systemctl is-enabled <service>
#
# Package name and systemd service name can be different.
#
# =========================================================

SERVICE_SYSTEMD_NAMES = {
    SERVICE_SSH: "ssh",
    SERVICE_FTP: "vsftpd",
    SERVICE_NFS: "nfs-server",
    SERVICE_SAMBA: "smbd",
    SERVICE_APACHE: "apache2",
    SERVICE_DNS: "named",
    SERVICE_MYSQL: "mysql",
}


# =========================================================
# Supported Service IDs
# =========================================================
#
# The order here controls the order in which services
# appear in the application.
#
# =========================================================

SUPPORTED_SERVICES = (
    SERVICE_SSH,
    SERVICE_FTP,
    SERVICE_NFS,
    SERVICE_SAMBA,
    SERVICE_APACHE,
    SERVICE_DNS,
    SERVICE_MYSQL,
)


# =========================================================
# Supported Operations
# =========================================================
#
# Runtime "status" is intentionally removed because the
# GUI no longer contains a STATUS column.
#
# Installation and startup information are handled
# separately by the ServiceManager.
#
# =========================================================

OP_INSTALL = "install"
OP_START = "start"
OP_STOP = "stop"
OP_RESTART = "restart"
OP_ENABLE = "enable"
OP_DISABLE = "disable"


SERVICE_OPERATIONS = (
    OP_INSTALL,
    OP_START,
    OP_STOP,
    OP_RESTART,
    OP_ENABLE,
    OP_DISABLE,
)


# =========================================================
# Installation States
# =========================================================

INSTALLATION_INSTALLED = "installed"
INSTALLATION_NOT_INSTALLED = "not_installed"
INSTALLATION_UNKNOWN = "unknown"


# =========================================================
# Startup States
# =========================================================

STARTUP_ENABLED = "enabled"
STARTUP_DISABLED = "disabled"
STARTUP_STATIC = "static"
STARTUP_MASKED = "masked"
STARTUP_UNKNOWN = "unknown"


# =========================================================
# UI Text
# =========================================================

READY_MESSAGE = "Ready"

INSTALLED_TEXT = "Installed"

NOT_INSTALLED_TEXT = "Not Installed"

ENABLED_TEXT = "Enabled"

DISABLED_TEXT = "Disabled"

STATIC_TEXT = "Static"

MASKED_TEXT = "Masked"

UNKNOWN_TEXT = "Unknown"


# =========================================================
# Helper Mappings
# =========================================================
#
# These mappings provide a single source of truth for the
# service configuration.
#
# =========================================================

SERVICE_CONFIG = {
    SERVICE_SSH: {
        "display_name": SERVICE_DISPLAY_NAMES[SERVICE_SSH],
        "package_name": SERVICE_PACKAGES[SERVICE_SSH],
        "systemd_name": SERVICE_SYSTEMD_NAMES[SERVICE_SSH],
    },

    SERVICE_FTP: {
        "display_name": SERVICE_DISPLAY_NAMES[SERVICE_FTP],
        "package_name": SERVICE_PACKAGES[SERVICE_FTP],
        "systemd_name": SERVICE_SYSTEMD_NAMES[SERVICE_FTP],
    },

    SERVICE_NFS: {
        "display_name": SERVICE_DISPLAY_NAMES[SERVICE_NFS],
        "package_name": SERVICE_PACKAGES[SERVICE_NFS],
        "systemd_name": SERVICE_SYSTEMD_NAMES[SERVICE_NFS],
    },

    SERVICE_SAMBA: {
        "display_name": SERVICE_DISPLAY_NAMES[SERVICE_SAMBA],
        "package_name": SERVICE_PACKAGES[SERVICE_SAMBA],
        "systemd_name": SERVICE_SYSTEMD_NAMES[SERVICE_SAMBA],
    },

    SERVICE_APACHE: {
        "display_name": SERVICE_DISPLAY_NAMES[SERVICE_APACHE],
        "package_name": SERVICE_PACKAGES[SERVICE_APACHE],
        "systemd_name": SERVICE_SYSTEMD_NAMES[SERVICE_APACHE],
    },

    SERVICE_DNS: {
        "display_name": SERVICE_DISPLAY_NAMES[SERVICE_DNS],
        "package_name": SERVICE_PACKAGES[SERVICE_DNS],
        "systemd_name": SERVICE_SYSTEMD_NAMES[SERVICE_DNS],
    },

    SERVICE_MYSQL: {
        "display_name": SERVICE_DISPLAY_NAMES[SERVICE_MYSQL],
        "package_name": SERVICE_PACKAGES[SERVICE_MYSQL],
        "systemd_name": SERVICE_SYSTEMD_NAMES[SERVICE_MYSQL],
    },
}