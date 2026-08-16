from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from app.services.command_runner import CommandRunner

from app.utils.constants import (
    SERVICE_APACHE,
    SERVICE_DISPLAY_NAMES,
    SERVICE_DNS,
    SERVICE_FTP,
    SERVICE_MYSQL,
    SERVICE_NFS,
    SERVICE_PACKAGES,
    SERVICE_SAMBA,
    SERVICE_SSH,
    SERVICE_SYSTEMD_NAMES,
)


# =========================================================
# Installation Status
# =========================================================


class InstallationStatus(str, Enum):
    """
    Installation state of a service.
    """

    INSTALLED = "installed"
    NOT_INSTALLED = "not_installed"
    UNKNOWN = "unknown"


# =========================================================
# Startup Status
# =========================================================


class StartupStatus(str, Enum):
    """
    Boot/startup state of a service.
    """

    ENABLED = "enabled"
    DISABLED = "disabled"
    STATIC = "static"
    MASKED = "masked"
    UNKNOWN = "unknown"


# =========================================================
# Service Definition
# =========================================================


@dataclass(frozen=True)
class ServiceDefinition:
    """
    Definition of a supported Linux network service.

    service_id:
        Internal application identifier.

    name:
        Human-readable service name.

    service_name:
        Actual systemd service name.

    package_name:
        Actual APT package name.
    """

    service_id: str
    name: str
    service_name: str
    package_name: str


# =========================================================
# Service Result
# =========================================================


@dataclass
class ServiceResult:
    """
    Standard result returned by service operations.
    """

    success: bool
    message: str
    output: str = ""
    error: str = ""


# =========================================================
# Service Manager
# =========================================================


class ServiceManager:
    """
    Main Linux network service management layer.

    Supported services:
        SSH / OpenSSH
        FTP
        NFS
        Samba
        Apache
        DNS
        MySQL

    DHCP is intentionally NOT supported.

    Responsibilities:
        1. Maintain supported service definitions.
        2. Keep APT package names separate from systemd names.
        3. Generate Linux commands.
        4. Execute commands through CommandRunner.
        5. Provide command preview / dry-run support.
        6. Parse installation status.
        7. Parse startup/enable status.

    Runtime service status is intentionally not part of
    this manager because the GUI no longer contains a
    runtime STATUS column.
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(
        self,
        command_runner: Optional[CommandRunner] = None,
    ) -> None:

        # -------------------------------------------------
        # Use supplied runner when provided.
        # -------------------------------------------------

        if command_runner is not None:

            self.command_runner = command_runner

        else:

            # -------------------------------------------------
            # Detect platform first.
            #
            # CommandRunner protects Windows execution.
            # Real command execution is enabled only on Linux.
            # -------------------------------------------------

            runner = CommandRunner()

            linux_execution = bool(
                runner.platform_info.is_linux
            )

            runner.execution_enabled = linux_execution

            self.command_runner = runner

        # -------------------------------------------------
        # Load supported services.
        # -------------------------------------------------

        self.services = self._load_services()

    # =====================================================
    # SERVICE DEFINITIONS
    # =====================================================

    @staticmethod
    def _load_services() -> dict[
        str,
        ServiceDefinition,
    ]:
        """
        Load all supported network services.

        DHCP is intentionally excluded.
        """

        service_ids = (
            SERVICE_SSH,
            SERVICE_FTP,
            SERVICE_NFS,
            SERVICE_SAMBA,
            SERVICE_APACHE,
            SERVICE_DNS,
            SERVICE_MYSQL,
        )

        services: dict[
            str,
            ServiceDefinition,
        ] = {}

        for service_id in service_ids:

            display_name = (
                SERVICE_DISPLAY_NAMES.get(
                    service_id
                )
            )

            package_name = (
                SERVICE_PACKAGES.get(
                    service_id
                )
            )

            systemd_name = (
                SERVICE_SYSTEMD_NAMES.get(
                    service_id
                )
            )

            # -------------------------------------------------
            # Invalid configuration protection
            # -------------------------------------------------

            if not display_name:
                continue

            if not package_name:
                continue

            if not systemd_name:
                continue

            services[service_id] = (
                ServiceDefinition(
                    service_id=service_id,
                    name=display_name,
                    service_name=systemd_name,
                    package_name=package_name,
                )
            )

        return services

    # =====================================================
    # GET SERVICE
    # =====================================================

    def get_service(
        self,
        service_id: str,
    ) -> Optional[ServiceDefinition]:
        """
        Return a service definition.
        """

        return self.services.get(
            service_id
        )

    # =====================================================
    # GET ALL SERVICES
    # =====================================================

    def get_all_services(
        self,
    ) -> list[ServiceDefinition]:
        """
        Return all supported services.
        """

        return list(
            self.services.values()
        )

    # =====================================================
    # GET PLATFORM INFORMATION
    # =====================================================

    def get_platform_info(self):
        """
        Return platform information used by CommandRunner.
        """

        return self.command_runner.platform_info

    # =====================================================
    # EXECUTION ENABLED
    # =====================================================

    def is_execution_enabled(self) -> bool:
        """
        Return whether command execution is enabled.
        """

        return bool(
            self.command_runner.execution_enabled
        )

    # =====================================================
    # ENABLE EXECUTION
    # =====================================================

    def enable_execution(self) -> None:
        """
        Enable command execution.

        CommandRunner still performs platform and
        required-tool safety checks.
        """

        self.command_runner.enable_execution()

    # =====================================================
    # DISABLE EXECUTION
    # =====================================================

    def disable_execution(self) -> None:
        """
        Disable command execution.
        """

        self.command_runner.disable_execution()

    # =====================================================
    # INSTALL
    # =====================================================

    def install(
        self,
        service_id: str,
    ) -> ServiceResult:
        """
        Install a service package using APT.

        Example:

            sudo apt install -y openssh-server
        """

        service = self.get_service(
            service_id
        )

        if service is None:

            return ServiceResult(
                success=False,
                message="Service not found.",
            )

        command = [
            "apt",
            "install",
            "-y",
            service.package_name,
        ]

        result = (
            self.command_runner.run(
                command,
                require_sudo=True,
            )
        )

        return self._convert_result(
            result,
            f"Install {service.name}",
        )

    # =====================================================
    # INSTALLATION STATUS
    # =====================================================

    def installation_status(
        self,
        service_id: str,
    ) -> ServiceResult:
        """
        Check whether the APT package is installed.

        Uses:

            dpkg-query -W -f=${Status} <package>

        dpkg-query can return a non-zero code when a
        package is not installed, so the output is parsed
        before treating the command as a real failure.
        """

        service = self.get_service(
            service_id
        )

        if service is None:

            return ServiceResult(
                success=False,
                message="Service not found.",
            )

        command = [
            "dpkg-query",
            "-W",
            "-f=${Status}",
            service.package_name,
        ]

        result = (
            self.command_runner.run(
                command,
                require_sudo=False,
            )
        )

        output = (
            result.stdout
            .strip()
            .lower()
        )

        error_output = (
            result.stderr
            .strip()
            .lower()
        )

        # -------------------------------------------------
        # Installed
        # -------------------------------------------------

        if "install ok installed" in output:

            return ServiceResult(
                success=True,
                message=(
                    f"{service.name} is installed."
                ),
                output=(
                    InstallationStatus.INSTALLED.value
                ),
                error=result.stderr,
            )

        # -------------------------------------------------
        # Package not installed
        # -------------------------------------------------

        not_installed_indicators = (
            "no packages found",
            "package '",
            "is not installed",
            "dpkg-query: no path found",
            "dpkg-query: no packages found",
        )

        if any(
            indicator in error_output
            for indicator in not_installed_indicators
        ):

            return ServiceResult(
                success=True,
                message=(
                    f"{service.name} is not installed."
                ),
                output=(
                    InstallationStatus.NOT_INSTALLED.value
                ),
                error=result.stderr,
            )

        # -------------------------------------------------
        # Unknown command failure
        # -------------------------------------------------

        if not result.success:

            return ServiceResult(
                success=False,
                message=result.message,
                output=result.stdout,
                error=result.stderr,
            )

        # -------------------------------------------------
        # Unknown package state
        # -------------------------------------------------

        return ServiceResult(
            success=True,
            message=(
                f"{service.name} installation state "
                "is unknown."
            ),
            output=(
                InstallationStatus.UNKNOWN.value
            ),
            error=result.stderr,
        )

    # =====================================================
    # START
    # =====================================================

    def start(
        self,
        service_id: str,
    ) -> ServiceResult:
        """
        Start a service using its systemd name.
        """

        service = self.get_service(
            service_id
        )

        if service is None:

            return ServiceResult(
                success=False,
                message="Service not found.",
            )

        command = [
            "systemctl",
            "start",
            service.service_name,
        ]

        result = (
            self.command_runner.run(
                command,
                require_sudo=True,
            )
        )

        return self._convert_result(
            result,
            f"Start {service.name}",
        )

    # =====================================================
    # STOP
    # =====================================================

    def stop(
        self,
        service_id: str,
    ) -> ServiceResult:
        """
        Stop a service using its systemd name.
        """

        service = self.get_service(
            service_id
        )

        if service is None:

            return ServiceResult(
                success=False,
                message="Service not found.",
            )

        command = [
            "systemctl",
            "stop",
            service.service_name,
        ]

        result = (
            self.command_runner.run(
                command,
                require_sudo=True,
            )
        )

        return self._convert_result(
            result,
            f"Stop {service.name}",
        )

    # =====================================================
    # RESTART
    # =====================================================

    def restart(
        self,
        service_id: str,
    ) -> ServiceResult:
        """
        Restart a service using its systemd name.
        """

        service = self.get_service(
            service_id
        )

        if service is None:

            return ServiceResult(
                success=False,
                message="Service not found.",
            )

        command = [
            "systemctl",
            "restart",
            service.service_name,
        ]

        result = (
            self.command_runner.run(
                command,
                require_sudo=True,
            )
        )

        return self._convert_result(
            result,
            f"Restart {service.name}",
        )

    # =====================================================
    # ENABLE
    # =====================================================

    def enable(
        self,
        service_id: str,
    ) -> ServiceResult:
        """
        Enable a service at system boot.
        """

        service = self.get_service(
            service_id
        )

        if service is None:

            return ServiceResult(
                success=False,
                message="Service not found.",
            )

        command = [
            "systemctl",
            "enable",
            service.service_name,
        ]

        result = (
            self.command_runner.run(
                command,
                require_sudo=True,
            )
        )

        return self._convert_result(
            result,
            f"Enable {service.name}",
        )

    # =====================================================
    # DISABLE
    # =====================================================

    def disable(
        self,
        service_id: str,
    ) -> ServiceResult:
        """
        Disable a service from automatic boot.
        """

        service = self.get_service(
            service_id
        )

        if service is None:

            return ServiceResult(
                success=False,
                message="Service not found.",
            )

        command = [
            "systemctl",
            "disable",
            service.service_name,
        ]

        result = (
            self.command_runner.run(
                command,
                require_sudo=True,
            )
        )

        return self._convert_result(
            result,
            f"Disable {service.name}",
        )

    # =====================================================
    # STARTUP / ENABLED STATUS
    # =====================================================

    def enabled_status(
        self,
        service_id: str,
    ) -> ServiceResult:
        """
        Check whether a service starts automatically
        during system boot.

        Uses:

            systemctl is-enabled <service>
        """

        service = self.get_service(
            service_id
        )

        if service is None:

            return ServiceResult(
                success=False,
                message="Service not found.",
            )

        command = [
            "systemctl",
            "is-enabled",
            service.service_name,
        ]

        result = (
            self.command_runner.run(
                command,
                require_sudo=False,
            )
        )

        output = (
            result.stdout
            .strip()
            .lower()
        )

        error_output = (
            result.stderr
            .strip()
            .lower()
        )

        # -------------------------------------------------
        # ENABLED
        # -------------------------------------------------

        if output == "enabled":

            return ServiceResult(
                success=True,
                message=(
                    f"{service.name} is enabled."
                ),
                output=(
                    StartupStatus.ENABLED.value
                ),
                error=result.stderr,
            )

        # -------------------------------------------------
        # DISABLED
        # -------------------------------------------------

        if output == "disabled":

            return ServiceResult(
                success=True,
                message=(
                    f"{service.name} is disabled."
                ),
                output=(
                    StartupStatus.DISABLED.value
                ),
                error=result.stderr,
            )

        # -------------------------------------------------
        # STATIC
        # -------------------------------------------------

        if output == "static":

            return ServiceResult(
                success=True,
                message=(
                    f"{service.name} is static."
                ),
                output=(
                    StartupStatus.STATIC.value
                ),
                error=result.stderr,
            )

        # -------------------------------------------------
        # MASKED
        # -------------------------------------------------

        if output == "masked":

            return ServiceResult(
                success=True,
                message=(
                    f"{service.name} is masked."
                ),
                output=(
                    StartupStatus.MASKED.value
                ),
                error=result.stderr,
            )

        # -------------------------------------------------
        # NOT FOUND
        # -------------------------------------------------

        if (
            "not-found" in error_output
            or "not found" in error_output
            or "could not be found" in error_output
        ):

            return ServiceResult(
                success=True,
                message=(
                    f"{service.name} startup state "
                    "is unknown."
                ),
                output=(
                    StartupStatus.UNKNOWN.value
                ),
                error=result.stderr,
            )

        # -------------------------------------------------
        # Known state returned through stdout
        # -------------------------------------------------

        if output:

            known_states = {
                StartupStatus.ENABLED.value,
                StartupStatus.DISABLED.value,
                StartupStatus.STATIC.value,
                StartupStatus.MASKED.value,
            }

            if output in known_states:

                return ServiceResult(
                    success=True,
                    message=(
                        f"{service.name} startup state "
                        f"is {output}."
                    ),
                    output=output,
                    error=result.stderr,
                )

        # -------------------------------------------------
        # Actual command failure
        # -------------------------------------------------

        if not result.success:

            return ServiceResult(
                success=False,
                message=result.message,
                output=result.stdout,
                error=result.stderr,
            )

        # -------------------------------------------------
        # Unknown
        # -------------------------------------------------

        return ServiceResult(
            success=True,
            message=(
                f"{service.name} startup state "
                "is unknown."
            ),
            output=(
                StartupStatus.UNKNOWN.value
            ),
            error=result.stderr,
        )

    # =====================================================
    # SERVICE COMMAND
    # =====================================================

    def get_service_command(
        self,
        action: str,
        service_id: str,
    ) -> Optional[list[str]]:
        """
        Prepare a Linux command without executing it.

        Supported actions:

            install
            start
            stop
            restart
            enable
            disable
            enabled_status
            startup_status
            installation_status
            install_status

        Runtime "status" is intentionally not supported
        because the GUI no longer has a STATUS column.
        """

        service = self.get_service(
            service_id
        )

        if service is None:
            return None

        normalized_action = (
            action.strip().lower()
        )

        # =================================================
        # INSTALL
        # =================================================

        if normalized_action == "install":

            return [
                "apt",
                "install",
                "-y",
                service.package_name,
            ]

        # =================================================
        # START
        # =================================================

        if normalized_action == "start":

            return [
                "systemctl",
                "start",
                service.service_name,
            ]

        # =================================================
        # STOP
        # =================================================

        if normalized_action == "stop":

            return [
                "systemctl",
                "stop",
                service.service_name,
            ]

        # =================================================
        # RESTART
        # =================================================

        if normalized_action == "restart":

            return [
                "systemctl",
                "restart",
                service.service_name,
            ]

        # =================================================
        # ENABLE
        # =================================================

        if normalized_action == "enable":

            return [
                "systemctl",
                "enable",
                service.service_name,
            ]

        # =================================================
        # DISABLE
        # =================================================

        if normalized_action == "disable":

            return [
                "systemctl",
                "disable",
                service.service_name,
            ]

        # =================================================
        # STARTUP STATUS
        # =================================================

        if normalized_action in (
            "enabled_status",
            "startup_status",
        ):

            return [
                "systemctl",
                "is-enabled",
                service.service_name,
            ]

        # =================================================
        # INSTALLATION STATUS
        # =================================================

        if normalized_action in (
            "installation_status",
            "install_status",
        ):

            return [
                "dpkg-query",
                "-W",
                "-f=${Status}",
                service.package_name,
            ]

        # =================================================
        # UNKNOWN ACTION
        # =================================================

        return None

    # =====================================================
    # COMMAND PREVIEW TEXT
    # =====================================================

    def get_service_command_text(
        self,
        action: str,
        service_id: str,
    ) -> Optional[str]:
        """
        Return the command as readable text.

        Examples:

            sudo systemctl start ssh

            sudo apt install -y openssh-server

            systemctl is-enabled ssh
        """

        command = (
            self.get_service_command(
                action,
                service_id,
            )
        )

        if command is None:
            return None

        normalized_action = (
            action.strip().lower()
        )

        sudo_actions = {
            "install",
            "start",
            "stop",
            "restart",
            "enable",
            "disable",
        }

        command_text = (
            " ".join(command)
        )

        if normalized_action in sudo_actions:

            return (
                "sudo "
                + command_text
            )

        return command_text

    # =====================================================
    # PREVIEW
    # =====================================================

    def preview(
        self,
        action: str,
        service_id: str,
    ) -> ServiceResult:
        """
        Generate a command preview.

        No command is executed.
        """

        service = self.get_service(
            service_id
        )

        if service is None:

            return ServiceResult(
                success=False,
                message="Service not found.",
            )

        command = (
            self.get_service_command(
                action,
                service_id,
            )
        )

        if command is None:

            return ServiceResult(
                success=False,
                message=(
                    f"Unknown service action: {action}"
                ),
            )

        command_result = (
            self.command_runner.preview(
                command,
                require_sudo=(
                    action.strip().lower()
                    in {
                        "install",
                        "start",
                        "stop",
                        "restart",
                        "enable",
                        "disable",
                    }
                ),
            )
        )

        if not command_result.success:

            return ServiceResult(
                success=False,
                message=command_result.message,
                output=command_result.stdout,
                error=command_result.stderr,
            )

        return ServiceResult(
            success=True,
            message=(
                f"Preview: {service.name} "
                f"{action.strip().lower()}"
            ),
            output=command_result.stdout,
            error=command_result.stderr,
        )

    # =====================================================
    # DRY RUN
    # =====================================================

    def dry_run(
        self,
        action: str,
        service_id: str,
    ) -> ServiceResult:
        """
        Generate a ServiceResult containing the command
        that would be executed.

        No command is executed.
        """

        return self.preview(
            action,
            service_id,
        )

    # =====================================================
    # INSTALLATION CHECK ALIAS
    # =====================================================

    def is_installed(
        self,
        service_id: str,
    ) -> ServiceResult:
        """
        Convenience wrapper around installation_status().
        """

        return self.installation_status(
            service_id
        )

    # =====================================================
    # STARTUP STATUS ALIAS
    # =====================================================

    def startup_status(
        self,
        service_id: str,
    ) -> ServiceResult:
        """
        Convenience wrapper around enabled_status().
        """

        return self.enabled_status(
            service_id
        )

    # =====================================================
    # RESULT CONVERSION
    # =====================================================

    @staticmethod
    def _convert_result(
        result,
        operation: str,
    ) -> ServiceResult:
        """
        Convert CommandRunner result into ServiceResult.
        """

        if result.success:

            return ServiceResult(
                success=True,
                message=(
                    f"{operation} completed successfully."
                ),
                output=result.stdout,
                error=result.stderr,
            )

        return ServiceResult(
            success=False,
            message=result.message,
            output=result.stdout,
            error=result.stderr,
        )