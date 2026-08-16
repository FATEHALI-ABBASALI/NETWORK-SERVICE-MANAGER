from __future__ import annotations

import os
import platform
import shutil
from dataclasses import dataclass


# =========================================================
# Platform Information
# =========================================================


@dataclass(frozen=True)
class PlatformInfo:
    """
    Information about the operating environment.

    This class only stores platform information.

    It does not execute any Linux service-management
    command.
    """

    operating_system: str

    is_windows: bool

    is_linux: bool

    is_ubuntu: bool

    has_systemctl: bool

    has_apt: bool

    has_sudo: bool

    @property
    def can_execute_linux_services(self) -> bool:
        """
        Return True only when Linux service-management
        commands can be executed safely.

        Required tools:

            systemctl
            apt
            sudo
        """

        return (
            self.is_linux
            and self.has_systemctl
            and self.has_apt
            and self.has_sudo
        )


# =========================================================
# Platform Detector
# =========================================================


class PlatformDetector:
    """
    Detect the current operating environment.

    Supported development/target environments:

        Windows
        Linux
        Ubuntu Linux

    This class does not execute service-management
    commands such as:

        start
        stop
        restart
        install
        enable
        disable
    """

    # =====================================================
    # DETECT PLATFORM
    # =====================================================

    @staticmethod
    def detect() -> PlatformInfo:
        """
        Detect the current operating system and required
        Linux administration tools.
        """

        # -------------------------------------------------
        # Operating System
        # -------------------------------------------------

        operating_system = platform.system()

        is_windows = (
            operating_system == "Windows"
        )

        is_linux = (
            operating_system == "Linux"
        )

        # -------------------------------------------------
        # Ubuntu Detection
        # -------------------------------------------------

        is_ubuntu = False

        if is_linux:
            is_ubuntu = (
                PlatformDetector._is_ubuntu()
            )

        # -------------------------------------------------
        # Required Linux Tools
        # -------------------------------------------------

        has_systemctl = (
            shutil.which("systemctl") is not None
        )

        has_apt = (
            shutil.which("apt") is not None
        )

        has_sudo = (
            shutil.which("sudo") is not None
        )

        # -------------------------------------------------
        # Platform Information
        # -------------------------------------------------

        return PlatformInfo(
            operating_system=operating_system,
            is_windows=is_windows,
            is_linux=is_linux,
            is_ubuntu=is_ubuntu,
            has_systemctl=has_systemctl,
            has_apt=has_apt,
            has_sudo=has_sudo,
        )

    # =====================================================
    # UBUNTU DETECTION
    # =====================================================

    @staticmethod
    def _is_ubuntu() -> bool:
        """
        Detect Ubuntu using /etc/os-release.

        No service-management command is executed.

        Returns:
            True  -> Ubuntu detected
            False -> Ubuntu not detected
        """

        os_release = "/etc/os-release"

        # -------------------------------------------------
        # Check File
        # -------------------------------------------------

        if not os.path.exists(
            os_release
        ):
            return False

        # -------------------------------------------------
        # Read OS Information
        # -------------------------------------------------

        try:

            with open(
                os_release,
                "r",
                encoding="utf-8",
            ) as file:

                content = (
                    file.read()
                    .lower()
                )

        except OSError:

            return False

        # -------------------------------------------------
        # Ubuntu Identification
        # -------------------------------------------------

        return (
            "id=ubuntu" in content
            or "id_like=ubuntu" in content
        )


# =========================================================
# Convenience Function
# =========================================================


def get_platform_info() -> PlatformInfo:
    """
    Return detected platform information.

    This is the main helper used by the application.
    """

    return PlatformDetector.detect()