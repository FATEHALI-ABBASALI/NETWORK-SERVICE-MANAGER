from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from typing import Sequence

from app.utils.platform import (
    PlatformInfo,
    get_platform_info,
)


# =========================================================
# Command Result
# =========================================================

@dataclass
class CommandResult:
    """
    Standard result returned after command execution.
    """

    success: bool
    return_code: int
    stdout: str = ""
    stderr: str = ""
    message: str = ""


# =========================================================
# Command Runner
# =========================================================

class CommandRunner:
    """
    Centralized command execution layer.

    Safety policy
    -------------

    Windows:
        - Linux commands are never executed.
        - Preview remains available.

    Linux:
        - Execution is allowed only when:
            * execution_enabled=True
            * Linux platform is detected
            * required tools are available

    Ubuntu:
        - Supports apt / apt-get
        - Supports systemctl
        - Supports sudo

    Security
    --------

    Commands are executed using subprocess without shell=True.

    This prevents shell interpretation of command arguments.

    Sudo commands use non-interactive mode during execution
    so the GUI cannot hang waiting for a password prompt.
    """

    # -----------------------------------------------------
    # Default timeout
    # -----------------------------------------------------

    DEFAULT_TIMEOUT = 120

    # -----------------------------------------------------
    # Maximum output size
    # -----------------------------------------------------

    MAX_OUTPUT_LENGTH = 10000

    def __init__(
        self,
        execution_enabled: bool = False,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:

        # -------------------------------------------------
        # Detect current platform
        # -------------------------------------------------

        self.platform_info: PlatformInfo = (
            get_platform_info()
        )

        # -------------------------------------------------
        # Safety switch
        # -------------------------------------------------

        self.execution_enabled = bool(
            execution_enabled
        )

        # -------------------------------------------------
        # Command timeout
        # -------------------------------------------------

        self.timeout = max(
            1,
            int(timeout),
        )

    # =====================================================
    # PLATFORM
    # =====================================================

    def refresh_platform_info(self) -> PlatformInfo:
        """
        Re-detect the current platform.

        Useful when the application environment changes
        or when the runner is initialized before platform
        detection is fully available.
        """

        self.platform_info = (
            get_platform_info()
        )

        return self.platform_info

    # =====================================================
    # LINUX EXECUTION AVAILABILITY
    # =====================================================

    def is_linux_execution_available(self) -> bool:
        """
        Return True when the current environment has the
        required Linux service-management tools.
        """

        return bool(
            self.platform_info.is_linux
            and self.platform_info.can_execute_linux_services
        )

    # =====================================================
    # REQUIRED TOOLS
    # =====================================================

    def get_missing_tools(self) -> list[str]:
        """
        Return required Linux tools that are unavailable.
        """

        missing_tools: list[str] = []

        # -------------------------------------------------
        # systemctl
        # -------------------------------------------------

        has_systemctl = bool(
            getattr(
                self.platform_info,
                "has_systemctl",
                False,
            )
        )

        if not has_systemctl:

            missing_tools.append(
                "systemctl"
            )

        # -------------------------------------------------
        # apt
        # -------------------------------------------------

        has_apt = bool(
            getattr(
                self.platform_info,
                "has_apt",
                False,
            )
        )

        if not has_apt:

            missing_tools.append(
                "apt"
            )

        # -------------------------------------------------
        # sudo
        # -------------------------------------------------

        has_sudo = bool(
            getattr(
                self.platform_info,
                "has_sudo",
                False,
            )
        )

        if not has_sudo:

            missing_tools.append(
                "sudo"
            )

        return missing_tools

    # =====================================================
    # BUILD COMMAND
    # =====================================================

    @staticmethod
    def build_command(
        command: Sequence[str],
        *,
        require_sudo: bool = False,
    ) -> list[str]:
        """
        Build the final command.

        Example:

            ["apt-get", "install", "-y", "apache2"]

        with require_sudo=True becomes:

            ["sudo", "apt-get", "install", "-y", "apache2"]
        """

        if not command:

            return []

        command_list = [
            str(part)
            for part in command
        ]

        # -------------------------------------------------
        # Add sudo when required
        # -------------------------------------------------

        if require_sudo:

            if command_list[0] != "sudo":

                command_list.insert(
                    0,
                    "sudo",
                )

        return command_list

    # =====================================================
    # COMMAND TEXT
    # =====================================================

    @staticmethod
    def command_to_text(
        command: Sequence[str],
    ) -> str:
        """
        Convert a command sequence into readable text.
        """

        return " ".join(
            str(part)
            for part in command
        )

    # =====================================================
    # COMMAND VALIDATION
    # =====================================================

    @staticmethod
    def validate_command(
        command: Sequence[str],
    ) -> tuple[bool, str]:
        """
        Validate a command before execution.
        """

        if not command:

            return (
                False,
                "No command was provided.",
            )

        for part in command:

            if part is None:

                return (
                    False,
                    "Command contains an invalid argument.",
                )

            if not isinstance(
                part,
                str,
            ):

                return (
                    False,
                    "Command arguments must be strings.",
                )

            if not part.strip():

                return (
                    False,
                    "Command contains an empty argument.",
                )

        return (
            True,
            "",
        )

    # =====================================================
    # EXECUTABLE CHECK
    # =====================================================

    @staticmethod
    def executable_exists(
        executable: str,
    ) -> bool:
        """
        Check whether an executable exists in PATH.
        """

        if not executable:

            return False

        return (
            shutil.which(
                executable
            )
            is not None
        )

    # =====================================================
    # PREVIEW
    # =====================================================

    def preview(
        self,
        command: Sequence[str],
        *,
        require_sudo: bool = False,
    ) -> CommandResult:
        """
        Generate a command preview.

        Preview NEVER executes the command.
        """

        valid, error = (
            self.validate_command(
                command
            )
        )

        if not valid:

            return CommandResult(
                success=False,
                return_code=-1,
                message=error,
            )

        final_command = (
            self.build_command(
                command,
                require_sudo=require_sudo,
            )
        )

        command_text = (
            self.command_to_text(
                final_command
            )
        )

        return CommandResult(
            success=True,
            return_code=0,
            stdout=command_text,
            message=command_text,
        )

    # =====================================================
    # RUN
    # =====================================================

    def run(
        self,
        command: Sequence[str],
        *,
        require_sudo: bool = False,
    ) -> CommandResult:
        """
        Execute a system command safely.

        Execution flow:

        1. Validate command.
        2. Build final command.
        3. Check execution_enabled.
        4. Check Linux platform.
        5. Check required Linux tools.
        6. Check executable.
        7. Execute using subprocess.
        8. Capture stdout/stderr.
        9. Apply timeout.
        10. Return CommandResult.
        """

        # =================================================
        # VALIDATE COMMAND
        # =================================================

        valid, error = (
            self.validate_command(
                command
            )
        )

        if not valid:

            return CommandResult(
                success=False,
                return_code=-1,
                message=error,
            )

        # =================================================
        # BUILD FINAL COMMAND
        # =================================================

        final_command = (
            self.build_command(
                command,
                require_sudo=require_sudo,
            )
        )

        command_text = (
            self.command_to_text(
                final_command
            )
        )

        # =================================================
        # SAFETY CHECK 1
        # =================================================

        if not self.execution_enabled:

            return CommandResult(
                success=False,
                return_code=-1,
                stdout=command_text,
                message=(
                    "Dry Run / Preview - command was "
                    "not executed: "
                    f"{command_text}"
                ),
            )

        # =================================================
        # REFRESH PLATFORM
        # =================================================

        self.refresh_platform_info()

        # =================================================
        # SAFETY CHECK 2
        # =================================================

        if not self.platform_info.is_linux:

            operating_system = str(
                getattr(
                    self.platform_info,
                    "operating_system",
                    "Unknown Platform",
                )
            )

            return CommandResult(
                success=False,
                return_code=-1,
                stdout=command_text,
                message=(
                    "Linux command execution is disabled "
                    f"on {operating_system}: "
                    f"{command_text}"
                ),
            )

        # =================================================
        # SAFETY CHECK 3
        # =================================================

        if not self.is_linux_execution_available():

            missing_tools = (
                self.get_missing_tools()
            )

            if missing_tools:

                missing_text = ", ".join(
                    missing_tools
                )

                return CommandResult(
                    success=False,
                    return_code=-1,
                    stdout=command_text,
                    message=(
                        "Linux service execution is "
                        "unavailable. Missing required "
                        f"tool(s): {missing_text}. "
                        f"Command: {command_text}"
                    ),
                )

            return CommandResult(
                success=False,
                return_code=-1,
                stdout=command_text,
                message=(
                    "Linux service execution is "
                    "currently unavailable. "
                    f"Command: {command_text}"
                ),
            )

        # =================================================
        # SAFETY CHECK 4
        # =================================================
        #
        # When sudo is required, verify sudo exists.
        # =================================================

        if require_sudo:

            if not self.executable_exists(
                "sudo"
            ):

                return CommandResult(
                    success=False,
                    return_code=127,
                    stdout=command_text,
                    message=(
                        "sudo was not found on the system. "
                        f"Command: {command_text}"
                    ),
                )

        # =================================================
        # EXECUTABLE CHECK
        # =================================================

        executable = final_command[0]

        # -------------------------------------------------
        # sudo is the executable when require_sudo=True.
        # The actual service command is therefore at index 1.
        # -------------------------------------------------

        executable_to_check = executable

        if executable == "sudo":

            if len(final_command) < 2:

                return CommandResult(
                    success=False,
                    return_code=-1,
                    stdout=command_text,
                    message=(
                        "Invalid sudo command."
                    ),
                )

            executable_to_check = (
                final_command[1]
            )

        if not self.executable_exists(
            executable_to_check
        ):

            return CommandResult(
                success=False,
                return_code=127,
                stdout=command_text,
                message=(
                    f"Required executable "
                    f"'{executable_to_check}' was not found. "
                    f"Command: {command_text}"
                ),
            )

        # =================================================
        # ACTUAL EXECUTION
        # =================================================

        execution_command = list(
            final_command
        )

        # -------------------------------------------------
        # Non-interactive sudo
        # -------------------------------------------------
        #
        # A GUI application must not hang waiting for a
        # terminal password prompt.
        #
        # -n makes sudo fail immediately if credentials
        # are not already available.
        #
        # This is safer than allowing a GUI subprocess to
        # remain blocked indefinitely.
        # -------------------------------------------------

        if (
            require_sudo
            and execution_command
            and execution_command[0] == "sudo"
        ):

            if "-n" not in execution_command:

                execution_command.insert(
                    1,
                    "-n",
                )

        execution_command_text = (
            self.command_to_text(
                execution_command
            )
        )

        # =================================================
        # SUBPROCESS
        # =================================================

        try:

            completed = (
                subprocess.run(
                    execution_command,
                    shell=False,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=self.timeout,
                    check=False,
                )
            )

        # =================================================
        # FILE / EXECUTABLE ERROR
        # =================================================

        except FileNotFoundError as exc:

            return CommandResult(
                success=False,
                return_code=127,
                stdout="",
                stderr=str(exc),
                message=(
                    "Command executable was not found: "
                    f"{execution_command_text}"
                ),
            )

        # =================================================
        # PERMISSION ERROR
        # =================================================

        except PermissionError as exc:

            return CommandResult(
                success=False,
                return_code=126,
                stdout="",
                stderr=str(exc),
                message=(
                    "Permission denied while executing "
                    f"command: {execution_command_text}"
                ),
            )

        # =================================================
        # TIMEOUT
        # =================================================

        except subprocess.TimeoutExpired as exc:

            stdout = (
                self._decode_timeout_output(
                    exc.stdout
                )
            )

            stderr = (
                self._decode_timeout_output(
                    exc.stderr
                )
            )

            return CommandResult(
                success=False,
                return_code=124,
                stdout=stdout,
                stderr=stderr,
                message=(
                    "Command timed out after "
                    f"{self.timeout} seconds: "
                    f"{execution_command_text}"
                ),
            )

        # =================================================
        # OS ERROR
        # =================================================

        except OSError as exc:

            return CommandResult(
                success=False,
                return_code=1,
                stdout="",
                stderr=str(exc),
                message=(
                    "Operating system error while "
                    "executing command: "
                    f"{execution_command_text}. "
                    f"Error: {exc}"
                ),
            )

        # =================================================
        # PROCESS RESULT
        # =================================================

        stdout = self._limit_output(
            completed.stdout
        )

        stderr = self._limit_output(
            completed.stderr
        )

        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        if completed.returncode == 0:

            message = (
                stdout.strip()
                or "Command executed successfully."
            )

            return CommandResult(
                success=True,
                return_code=completed.returncode,
                stdout=stdout,
                stderr=stderr,
                message=message,
            )

        # -------------------------------------------------
        # FAILURE
        # -------------------------------------------------

        error_message = (
            stderr.strip()
            or stdout.strip()
            or (
                "Command failed with return code "
                f"{completed.returncode}."
            )
        )

        return CommandResult(
            success=False,
            return_code=completed.returncode,
            stdout=stdout,
            stderr=stderr,
            message=(
                f"{error_message}"
            ),
        )

    # =====================================================
    # OUTPUT LIMIT
    # =====================================================

    @classmethod
    def _limit_output(
        cls,
        output: str | None,
    ) -> str:
        """
        Limit captured command output.

        Prevents an unexpectedly large command output from
        consuming excessive application memory.
        """

        if not output:

            return ""

        if len(output) <= cls.MAX_OUTPUT_LENGTH:

            return output

        return (
            output[: cls.MAX_OUTPUT_LENGTH]
            + "\n\n"
            "[Output truncated by Network Service Manager.]"
        )

    # =====================================================
    # TIMEOUT OUTPUT
    # =====================================================

    @staticmethod
    def _decode_timeout_output(
        output: str | bytes | None,
    ) -> str:
        """
        Normalize TimeoutExpired output.
        """

        if output is None:

            return ""

        if isinstance(
            output,
            bytes,
        ):

            return output.decode(
                "utf-8",
                errors="replace",
            )

        return str(
            output
        )

    # =====================================================
    # EXECUTION STATUS
    # =====================================================

    def get_execution_status(self) -> dict[str, object]:
        """
        Return a structured description of the current
        command execution environment.

        Useful for GUI diagnostics.
        """

        self.refresh_platform_info()

        missing_tools = (
            self.get_missing_tools()
        )

        return {
            "execution_enabled": (
                self.execution_enabled
            ),
            "is_linux": bool(
                self.platform_info.is_linux
            ),
            "is_ubuntu": bool(
                getattr(
                    self.platform_info,
                    "is_ubuntu",
                    False,
                )
            ),
            "can_execute": (
                self.is_linux_execution_available()
            ),
            "missing_tools": missing_tools,
            "operating_system": str(
                getattr(
                    self.platform_info,
                    "operating_system",
                    "Unknown",
                )
            ),
        }

    # =====================================================
    # ENABLE EXECUTION
    # =====================================================

    def enable_execution(self) -> None:
        """
        Enable command execution.

        IMPORTANT:
        The platform and required-tool checks still apply.
        """

        self.execution_enabled = True

    # =====================================================
    # DISABLE EXECUTION
    # =====================================================

    def disable_execution(self) -> None:
        """
        Disable command execution immediately.
        """

        self.execution_enabled = False