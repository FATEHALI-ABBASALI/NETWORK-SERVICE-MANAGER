from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from app.services.service_manager import ServiceManager
from app.utils.platform import PlatformInfo, get_platform_info


# =========================================================
# SUPPORTED SERVICES
# =========================================================
#
# DHCP intentionally removed.
#
# Total = 7
#
# 1. SSH / OpenSSH
# 2. FTP
# 3. NFS
# 4. Samba
# 5. Apache
# 6. DNS
# 7. MySQL
#
# =========================================================

SERVICES = [
    ("SSH / OpenSSH", "ssh"),
    ("FTP", "vsftpd"),
    ("NFS", "nfs-server"),
    ("Samba", "smbd"),
    ("Apache", "apache2"),
    ("DNS", "bind9"),
    ("MySQL", "mysql"),
]


# =========================================================
# MAIN WINDOW
# =========================================================


class MainWindow(QMainWindow):
    """
    Main Network Service Manager dashboard.

    DHCP is intentionally excluded.

    Table columns:

        SERVICE
        INSTALLATION
        STARTUP
        ACTIONS

    No separate STATUS column.
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(
            "Network Service Manager"
        )

        self.setMinimumSize(
            1100,
            700,
        )

        self.resize(
            1400,
            850,
        )

        # -------------------------------------------------
        # Platform
        # -------------------------------------------------

        self.platform_info: PlatformInfo = (
            get_platform_info()
        )

        # -------------------------------------------------
        # Service Manager
        # -------------------------------------------------

        self.service_manager = ServiceManager()

        # -------------------------------------------------
        # Build
        # -------------------------------------------------

        self._build_ui()

        self._update_platform_status()

        self._refresh_services()


    # =====================================================
    # BUILD UI
    # =====================================================

    def _build_ui(self) -> None:

        central = QWidget()

        central.setObjectName(
            "central_widget"
        )

        self.setCentralWidget(
            central
        )

        main_layout = QVBoxLayout(
            central
        )

        main_layout.setContentsMargins(
            24,
            20,
            24,
            12,
        )

        main_layout.setSpacing(
            12
        )

        # =================================================
        # HEADER
        # =================================================

        header = QHBoxLayout()

        header.setSpacing(
            15
        )

        title_layout = QVBoxLayout()

        title_layout.setSpacing(
            2
        )

        title = QLabel(
            "Network Service Manager"
        )

        title.setObjectName(
            "app_title"
        )

        subtitle = QLabel(
            "Manage Linux network services from one dashboard"
        )

        subtitle.setObjectName(
            "app_subtitle"
        )

        title_layout.addWidget(
            title
        )

        title_layout.addWidget(
            subtitle
        )

        header.addLayout(
            title_layout
        )

        header.addStretch()

        # -------------------------------------------------
        # Platform Badge
        # -------------------------------------------------

        self.system_label = QLabel(
            "●  Detecting Platform..."
        )

        self.system_label.setObjectName(
            "system_status"
        )

        self.system_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.system_label.setMinimumSize(
            220,
            44,
        )

        header.addWidget(
            self.system_label
        )

        main_layout.addLayout(
            header
        )

        # =================================================
        # INFO BAR
        # =================================================

        info_frame = QFrame()

        info_frame.setObjectName(
            "info_frame"
        )

        info_layout = QHBoxLayout(
            info_frame
        )

        info_layout.setContentsMargins(
            14,
            9,
            14,
            9,
        )

        info_layout.setSpacing(
            10
        )

        info_icon = QLabel(
            "ⓘ"
        )

        info_icon.setObjectName(
            "info_icon"
        )

        info_text = QLabel(
            "Manage installation and startup configuration "
            "for supported Linux network services."
        )

        info_text.setObjectName(
            "info_text"
        )

        info_layout.addWidget(
            info_icon
        )

        info_layout.addWidget(
            info_text,
            1,
        )

        main_layout.addWidget(
            info_frame
        )

        # =================================================
        # SUMMARY CARDS
        # =================================================

        cards_layout = QHBoxLayout()

        cards_layout.setSpacing(
            12
        )

        self.total_card = (
            self._create_summary_card(
                "TOTAL SERVICES",
                "7",
                "Supported services",
            )
        )

        self.installed_card = (
            self._create_summary_card(
                "INSTALLED",
                "0",
                "Packages installed",
            )
        )

        self.target_card = (
            self._create_summary_card(
                "TARGET",
                "Ubuntu",
                "Linux service platform",
            )
        )

        self.mode_card = (
            self._create_summary_card(
                "MODE",
                "Ready",
                "Application state",
            )
        )

        cards_layout.addWidget(
            self.total_card
        )

        cards_layout.addWidget(
            self.installed_card
        )

        cards_layout.addWidget(
            self.target_card
        )

        cards_layout.addWidget(
            self.mode_card
        )

        main_layout.addLayout(
            cards_layout
        )

        # =================================================
        # SERVICE PANEL
        # =================================================

        service_frame = QFrame()

        service_frame.setObjectName(
            "service_frame"
        )

        service_layout = QVBoxLayout(
            service_frame
        )

        service_layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        service_layout.setSpacing(
            10
        )

        # =================================================
        # SERVICE HEADER
        # =================================================

        service_header = QHBoxLayout()

        service_title_layout = QVBoxLayout()

        service_title_layout.setSpacing(
            1
        )

        section_title = QLabel(
            "Network Services"
        )

        section_title.setObjectName(
            "section_title"
        )

        section_description = QLabel(
            "Install, start, stop and configure Linux services"
        )

        section_description.setObjectName(
            "section_description"
        )

        service_title_layout.addWidget(
            section_title
        )

        service_title_layout.addWidget(
            section_description
        )

        service_header.addLayout(
            service_title_layout
        )

        service_header.addStretch()

        # -------------------------------------------------
        # Refresh
        # -------------------------------------------------

        refresh_button = QPushButton(
            "↻  Refresh"
        )

        refresh_button.setObjectName(
            "refresh_button"
        )

        refresh_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        refresh_button.setMinimumSize(
            105,
            38,
        )

        refresh_button.clicked.connect(
            self._refresh_services
        )

        service_header.addWidget(
            refresh_button
        )

        service_layout.addLayout(
            service_header
        )

        # =================================================
        # TABLE
        # =================================================

        self.service_table = QTableWidget()

        self.service_table.setObjectName(
            "service_table"
        )

        # -------------------------------------------------
        # EXACTLY 7 SERVICES
        # -------------------------------------------------

        self.service_table.setRowCount(
            len(SERVICES)
        )

        # -------------------------------------------------
        # EXACTLY 4 COLUMNS
        # -------------------------------------------------

        self.service_table.setColumnCount(
            4
        )

        self.service_table.setHorizontalHeaderLabels(
            [
                "SERVICE",
                "INSTALLATION",
                "STARTUP",
                "ACTIONS",
            ]
        )

        # -------------------------------------------------
        # Behaviour
        # -------------------------------------------------

        self.service_table.verticalHeader().setVisible(
            False
        )

        self.service_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.service_table.setSelectionMode(
            QTableWidget.SelectionMode.NoSelection
        )

        self.service_table.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        self.service_table.setShowGrid(
            False
        )

        self.service_table.setWordWrap(
            False
        )

        # -------------------------------------------------
        # IMPORTANT:
        # Proper vertical scrollbar
        # -------------------------------------------------

        # Always show the table scrollbar so all 7 services remain
        # accessible even when the application window is smaller.
        self.service_table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        self.service_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # -------------------------------------------------
        # Table minimum / preferred size
        # -------------------------------------------------

        # Keep the service table compact enough to require a vertical
        # scrollbar. This prevents the lower service rows from being
        # clipped by the main window while keeping the dashboard clean.
        self.service_table.setMinimumHeight(
            0
        )

        self.service_table.setMaximumHeight(
            315
        )

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        header = (
            self.service_table.horizontalHeader()
        )

        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        # Service
        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.Stretch,
        )

        # Installation
        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Fixed,
        )

        # Startup
        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.Fixed,
        )

        # Actions
        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.Stretch,
        )

        self.service_table.setColumnWidth(
            1,
            135,
        )

        self.service_table.setColumnWidth(
            2,
            120,
        )

        # -------------------------------------------------
        # Add ALL 7 rows
        # -------------------------------------------------

        for row, (
            service_name,
            service_id,
        ) in enumerate(
            SERVICES
        ):

            self._add_service_row(
                row,
                service_name,
                service_id,
            )

        service_layout.addWidget(
            self.service_table,
            1,
        )

        main_layout.addWidget(
            service_frame,
            1,
        )

        # =================================================
        # FOOTER
        # =================================================

        footer = QHBoxLayout()

        footer.setContentsMargins(
            2,
            0,
            2,
            0,
        )

        footer_label = QLabel(
            "Network Service Manager  •  v1.0.0"
        )

        footer_label.setObjectName(
            "footer"
        )

        footer.addWidget(
            footer_label
        )

        footer.addStretch()

        self.footer_status = QLabel(
            "Ready"
        )

        self.footer_status.setObjectName(
            "footer_status"
        )

        footer.addWidget(
            self.footer_status
        )

        main_layout.addLayout(
            footer
        )

        # =================================================
        # DARK THEME
        # =================================================

        self._apply_dark_theme()


    # =====================================================
    # SUMMARY CARD
    # =====================================================

    @staticmethod
    def _create_summary_card(
        heading: str,
        value: str,
        description: str,
    ) -> QFrame:

        card = QFrame()

        card.setObjectName(
            "summary_card"
        )

        card.setMinimumHeight(
            88
        )

        layout = QVBoxLayout(
            card
        )

        layout.setContentsMargins(
            16,
            10,
            16,
            10,
        )

        layout.setSpacing(
            1
        )

        heading_label = QLabel(
            heading
        )

        heading_label.setObjectName(
            "card_heading"
        )

        value_label = QLabel(
            value
        )

        value_label.setObjectName(
            "card_value"
        )

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "card_description"
        )

        layout.addWidget(
            heading_label
        )

        layout.addWidget(
            value_label
        )

        layout.addWidget(
            description_label
        )

        return card


    # =====================================================
    # SET CARD VALUE
    # =====================================================

    @staticmethod
    def _set_card_value(
        card: QFrame,
        value: str,
    ) -> None:

        label = card.findChild(
            QLabel,
            "card_value",
        )

        if label:

            label.setText(
                value
            )


    # =====================================================
    # PLATFORM STATUS
    # =====================================================

    def _update_platform_status(self) -> None:

        info = self.platform_info

        is_windows = bool(
            getattr(
                info,
                "is_windows",
                False,
            )
        )

        is_linux = bool(
            getattr(
                info,
                "is_linux",
                False,
            )
        )

        is_ubuntu = bool(
            getattr(
                info,
                "is_ubuntu",
                False,
            )
        )

        can_execute = bool(
            getattr(
                info,
                "can_execute_linux_services",
                False,
            )
        )

        operating_system = str(
            getattr(
                info,
                "operating_system",
                "Unknown",
            )
        )

        if is_windows:

            self.system_label.setText(
                "●  Windows Development"
            )

            self.system_label.setProperty(
                "platform_state",
                "windows",
            )

            self._set_card_value(
                self.mode_card,
                "Dev",
            )

            self.footer_status.setText(
                "Windows development mode"
            )

        elif is_ubuntu and can_execute:

            self.system_label.setText(
                "●  Ubuntu Ready"
            )

            self.system_label.setProperty(
                "platform_state",
                "ubuntu",
            )

            self._set_card_value(
                self.mode_card,
                "Ready",
            )

            self.footer_status.setText(
                "Ubuntu detected • Service tools ready"
            )

        elif is_ubuntu:

            self.system_label.setText(
                "●  Ubuntu • Tools Missing"
            )

            self.system_label.setProperty(
                "platform_state",
                "warning",
            )

            self._set_card_value(
                self.mode_card,
                "Check",
            )

            self.footer_status.setText(
                "Ubuntu detected • Check required tools"
            )

        elif is_linux:

            self.system_label.setText(
                "●  Linux"
            )

            self.system_label.setProperty(
                "platform_state",
                "linux",
            )

            self._set_card_value(
                self.mode_card,
                "Linux",
            )

            self.footer_status.setText(
                "Linux detected"
            )

        else:

            self.system_label.setText(
                f"●  {operating_system}"
            )

            self.system_label.setProperty(
                "platform_state",
                "unknown",
            )

            self._set_card_value(
                self.mode_card,
                "N/A",
            )

        self.system_label.style().unpolish(
            self.system_label
        )

        self.system_label.style().polish(
            self.system_label
        )

        self.system_label.update()


    # =====================================================
    # ADD SERVICE ROW
    # =====================================================

    def _add_service_row(
        self,
        row: int,
        service_name: str,
        service_id: str,
    ) -> None:

        # =================================================
        # SERVICE
        # =================================================

        name_item = QTableWidgetItem(
            service_name
        )

        name_item.setData(
            Qt.ItemDataRole.UserRole,
            service_id,
        )

        name_item.setTextAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.service_table.setItem(
            row,
            0,
            name_item,
        )

        # =================================================
        # INSTALLATION
        # =================================================

        installation = QTableWidgetItem(
            "Unknown"
        )

        installation.setTextAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.service_table.setItem(
            row,
            1,
            installation,
        )

        # =================================================
        # STARTUP
        # =================================================

        startup = QTableWidgetItem(
            "Unknown"
        )

        startup.setTextAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.service_table.setItem(
            row,
            2,
            startup,
        )

        # =================================================
        # ACTIONS
        # =================================================

        action_widget = QWidget()

        action_layout = QHBoxLayout(
            action_widget
        )

        action_layout.setContentsMargins(
            4,
            4,
            4,
            4,
        )

        action_layout.setSpacing(
            4
        )

        # -------------------------------------------------
        # INSTALL
        # -------------------------------------------------

        install = self._create_action_button(
            "Install",
            "install_button",
            "Install service",
        )

        install.clicked.connect(
            lambda checked=False,
            sid=service_id:
            self._handle_service_action(
                "install",
                sid,
            )
        )

        action_layout.addWidget(
            install
        )

        # -------------------------------------------------
        # START
        # -------------------------------------------------

        start = self._create_action_button(
            "Start",
            "start_button",
            "Start service",
        )

        start.clicked.connect(
            lambda checked=False,
            sid=service_id:
            self._handle_service_action(
                "start",
                sid,
            )
        )

        action_layout.addWidget(
            start
        )

        # -------------------------------------------------
        # STOP
        # -------------------------------------------------

        stop = self._create_action_button(
            "Stop",
            "stop_button",
            "Stop service",
        )

        stop.clicked.connect(
            lambda checked=False,
            sid=service_id:
            self._handle_service_action(
                "stop",
                sid,
            )
        )

        action_layout.addWidget(
            stop
        )

        # -------------------------------------------------
        # RESTART
        # -------------------------------------------------

        restart = self._create_action_button(
            "Restart",
            "restart_button",
            "Restart service",
        )

        restart.clicked.connect(
            lambda checked=False,
            sid=service_id:
            self._handle_service_action(
                "restart",
                sid,
            )
        )

        action_layout.addWidget(
            restart
        )

        # -------------------------------------------------
        # ENABLE
        # -------------------------------------------------

        enable = self._create_action_button(
            "Enable",
            "enable_button",
            "Enable service at boot",
        )

        enable.clicked.connect(
            lambda checked=False,
            sid=service_id:
            self._handle_service_action(
                "enable",
                sid,
            )
        )

        action_layout.addWidget(
            enable
        )

        # -------------------------------------------------
        # DISABLE
        # -------------------------------------------------

        disable = self._create_action_button(
            "Disable",
            "disable_button",
            "Disable service at boot",
        )

        disable.clicked.connect(
            lambda checked=False,
            sid=service_id:
            self._handle_service_action(
                "disable",
                sid,
            )
        )

        action_layout.addWidget(
            disable
        )

        # -------------------------------------------------
        # PREVIEW
        # -------------------------------------------------

        preview = self._create_action_button(
            "Preview",
            "preview_button",
            "Preview commands",
        )

        preview.clicked.connect(
            lambda checked=False,
            sid=service_id:
            self._show_command_preview(
                sid
            )
        )

        action_layout.addWidget(
            preview
        )

        self.service_table.setCellWidget(
            row,
            3,
            action_widget,
        )

        # -------------------------------------------------
        # COMPACT ROW
        # -------------------------------------------------

        self.service_table.setRowHeight(
            row,
            48,
        )


    # =====================================================
    # ACTION BUTTON
    # =====================================================

    @staticmethod
    def _create_action_button(
        text: str,
        object_name: str,
        tooltip: str,
    ) -> QPushButton:

        button = QPushButton(
            text
        )

        button.setObjectName(
            object_name
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setToolTip(
            tooltip
        )

        button.setMinimumHeight(
            32
        )

        button.setMinimumWidth(
            60
        )

        button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        return button


    # =====================================================
    # SERVICE ACTION
    # =====================================================

    def _handle_service_action(
        self,
        action: str,
        service_id: str,
    ) -> None:

        service = (
            self.service_manager.get_service(
                service_id
            )
        )

        if service is None:

            self._show_error(
                "Service not found."
            )

            return

        operations = {
            "install": self.service_manager.install,
            "start": self.service_manager.start,
            "stop": self.service_manager.stop,
            "restart": self.service_manager.restart,
            "enable": self.service_manager.enable,
            "disable": self.service_manager.disable,
        }

        operation = operations.get(
            action
        )

        if operation is None:

            self._show_error(
                f"Unknown operation: {action}"
            )

            return

        self.footer_status.setText(
            f"Executing {action} for {service.name}..."
        )

        result = operation(
            service_id
        )

        self.footer_status.setText(
            result.message
        )

        if result.success:

            self._show_success(
                result.message
            )

        else:

            self._show_info(
                result.message
            )

        row = self._find_service_row(
            service_id
        )

        if row >= 0:

            self._refresh_installation_status(
                row,
                service_id,
            )

            self._refresh_startup_status(
                row,
                service_id,
            )

            self._update_summary_cards()


    # =====================================================
    # COMMAND PREVIEW
    # =====================================================

    def _show_command_preview(
        self,
        service_id: str,
    ) -> None:

        service = (
            self.service_manager.get_service(
                service_id
            )
        )

        if service is None:

            self._show_error(
                "Service not found."
            )

            return

        dialog = QDialog(
            self
        )

        dialog.setObjectName(
            "command_preview_dialog"
        )

        dialog.setWindowTitle(
            f"Command Preview • {service.name}"
        )

        dialog.setMinimumSize(
            760,
            560,
        )

        dialog.resize(
            850,
            620,
        )

        layout = QVBoxLayout(
            dialog
        )

        layout.setContentsMargins(
            22,
            22,
            22,
            22,
        )

        layout.setSpacing(
            12
        )

        title = QLabel(
            "Command Preview"
        )

        title.setObjectName(
            "preview_title"
        )

        layout.addWidget(
            title
        )

        description = QLabel(
            "Preview the Linux commands used by this service. "
            "No command is executed in preview mode."
        )

        description.setObjectName(
            "preview_description"
        )

        description.setWordWrap(
            True
        )

        layout.addWidget(
            description
        )

        # -------------------------------------------------
        # SERVICE INFO
        # -------------------------------------------------

        info_frame = QFrame()

        info_frame.setObjectName(
            "preview_info_frame"
        )

        info_layout = QVBoxLayout(
            info_frame
        )

        info_layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )

        labels = [
            f"Service: {service.name}",
            f"APT Package: {service.package_name}",
            f"systemd Service: {service.service_name}",
        ]

        for text in labels:

            label = QLabel(
                text
            )

            label.setObjectName(
                "preview_info"
            )

            info_layout.addWidget(
                label
            )

        layout.addWidget(
            info_frame
        )

        # -------------------------------------------------
        # COMMANDS
        # -------------------------------------------------

        commands_text = QTextEdit()

        commands_text.setObjectName(
            "command_preview_text"
        )

        commands_text.setReadOnly(
            True
        )

        commands_text.setLineWrapMode(
            QTextEdit.LineWrapMode.NoWrap
        )

        commands = [
            ("INSTALL", "install"),
            ("START", "start"),
            ("STOP", "stop"),
            ("RESTART", "restart"),
            ("ENABLE", "enable"),
            ("DISABLE", "disable"),
            (
                "STARTUP STATUS",
                "enabled_status",
            ),
            (
                "INSTALLATION STATUS",
                "installation_status",
            ),
        ]

        lines = []

        for label, operation in commands:

            command = (
                self.service_manager
                .get_service_command_text(
                    operation,
                    service_id,
                )
            )

            if command is None:

                command = "Command unavailable"

            lines.append(
                f"{label:<24} {command}"
            )

        commands_text.setPlainText(
            "\n".join(
                lines
            )
        )

        layout.addWidget(
            commands_text,
            1,
        )

        # -------------------------------------------------
        # DRY RUN
        # -------------------------------------------------

        dry_run = QLabel(
            "✓  Preview only • No command executed"
        )

        dry_run.setObjectName(
            "dry_run_label"
        )

        layout.addWidget(
            dry_run
        )

        # -------------------------------------------------
        # CLOSE
        # -------------------------------------------------

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close
        )

        buttons.rejected.connect(
            dialog.reject
        )

        layout.addWidget(
            buttons
        )

        dialog.exec()


    # =====================================================
    # REFRESH
    # =====================================================

    def _refresh_services(self) -> None:

        self.footer_status.setText(
            "Refreshing services..."
        )

        for row, (
            _,
            service_id,
        ) in enumerate(
            SERVICES
        ):

            self._refresh_installation_status(
                row,
                service_id,
            )

            self._refresh_startup_status(
                row,
                service_id,
            )

        self._update_summary_cards()

        self.footer_status.setText(
            "Services refreshed."
        )


    # =====================================================
    # INSTALLATION STATUS
    # =====================================================

    def _refresh_installation_status(
        self,
        row: int,
        service_id: str,
    ) -> None:

        result = (
            self.service_manager
            .installation_status(
                service_id
            )
        )

        item = (
            self.service_table.item(
                row,
                1,
            )
        )

        if item is None:
            return

        if not result.success:

            item.setText(
                "Unknown"
            )

            self._style_status_item(
                item,
                "unknown",
            )

            return

        status = (
            result.output
            .strip()
            .lower()
        )

        if status == "installed":

            item.setText(
                "✓ Installed"
            )

            self._style_status_item(
                item,
                "installed",
            )

        elif status == "not_installed":

            item.setText(
                "Not Installed"
            )

            self._style_status_item(
                item,
                "not_installed",
            )

        else:

            item.setText(
                "Unknown"
            )

            self._style_status_item(
                item,
                "unknown",
            )


    # =====================================================
    # STARTUP STATUS
    # =====================================================

    def _refresh_startup_status(
        self,
        row: int,
        service_id: str,
    ) -> None:

        result = (
            self.service_manager
            .enabled_status(
                service_id
            )
        )

        item = (
            self.service_table.item(
                row,
                2,
            )
        )

        if item is None:
            return

        if not result.success:

            item.setText(
                "Unknown"
            )

            self._style_status_item(
                item,
                "unknown",
            )

            return

        status = (
            result.output
            .strip()
            .lower()
        )

        if status == "enabled":

            item.setText(
                "✓ Enabled"
            )

            self._style_status_item(
                item,
                "enabled",
            )

        elif status == "disabled":

            item.setText(
                "Disabled"
            )

            self._style_status_item(
                item,
                "disabled",
            )

        elif status == "static":

            item.setText(
                "Static"
            )

            self._style_status_item(
                item,
                "static",
            )

        elif status == "masked":

            item.setText(
                "Masked"
            )

            self._style_status_item(
                item,
                "masked",
            )

        else:

            item.setText(
                "Unknown"
            )

            self._style_status_item(
                item,
                "unknown",
            )


    # =====================================================
    # STATUS STYLE
    # =====================================================

    @staticmethod
    def _style_status_item(
        item: QTableWidgetItem,
        status: str,
    ) -> None:

        font = QFont()

        font.setPointSize(
            10
        )

        font.setWeight(
            QFont.Weight.DemiBold
        )

        item.setFont(
            font
        )

        if status in (
            "installed",
            "enabled",
        ):

            item.setForeground(
                Qt.GlobalColor.green
            )

        elif status in (
            "not_installed",
            "disabled",
        ):

            item.setForeground(
                Qt.GlobalColor.lightGray
            )

        elif status == "masked":

            item.setForeground(
                Qt.GlobalColor.red
            )

        elif status == "static":

            item.setForeground(
                Qt.GlobalColor.cyan
            )

        else:

            item.setForeground(
                Qt.GlobalColor.gray
            )


    # =====================================================
    # FIND ROW
    # =====================================================

    @staticmethod
    def _find_service_row(
        service_id: str,
    ) -> int:

        for row, (
            _,
            current_id,
        ) in enumerate(
            SERVICES
        ):

            if current_id == service_id:

                return row

        return -1


    # =====================================================
    # UPDATE CARDS
    # =====================================================

    def _update_summary_cards(self) -> None:

        installed_count = 0

        for row in range(
            self.service_table.rowCount()
        ):

            item = (
                self.service_table.item(
                    row,
                    1,
                )
            )

            if item is None:
                continue

            text = (
                item.text()
                .strip()
                .lower()
            )

            if text in (
                "installed",
                "✓ installed",
            ):

                installed_count += 1

        self._set_card_value(
            self.installed_card,
            str(
                installed_count
            ),
        )

        self._set_card_value(
            self.total_card,
            "7",
        )


    # =====================================================
    # MESSAGE BOXES
    # =====================================================

    def _show_success(
        self,
        message: str,
    ) -> None:

        QMessageBox.information(
            self,
            "Operation Successful",
            message,
        )


    def _show_info(
        self,
        message: str,
    ) -> None:

        QMessageBox.information(
            self,
            "Network Service Manager",
            message,
        )


    def _show_error(
        self,
        message: str,
    ) -> None:

        QMessageBox.critical(
            self,
            "Error",
            message,
        )


    # =====================================================
    # DARK PROFESSIONAL THEME
    # =====================================================

    def _apply_dark_theme(self) -> None:

        self.setStyleSheet(
            """

            /* =================================================
               GLOBAL
               ================================================= */

            QMainWindow {
                background-color: #0b1120;
            }

            QWidget#central_widget {
                background-color: #0b1120;
            }

            QWidget {
                color: #e5e7eb;
                font-family: "Segoe UI", Arial, sans-serif;
            }


            /* =================================================
               HEADER
               ================================================= */

            QLabel#app_title {
                color: #f8fafc;
                font-size: 28px;
                font-weight: 750;
                padding: 0px;
            }

            QLabel#app_subtitle {
                color: #94a3b8;
                font-size: 13px;
            }


            /* =================================================
               PLATFORM BADGE
               ================================================= */

            QLabel#system_status {
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 700;
            }

            QLabel#system_status[platform_state="windows"] {
                color: #60a5fa;
                background-color: #172554;
                border: 1px solid #1d4ed8;
            }

            QLabel#system_status[platform_state="ubuntu"] {
                color: #34d399;
                background-color: #052e1b;
                border: 1px solid #047857;
            }

            QLabel#system_status[platform_state="warning"] {
                color: #fbbf24;
                background-color: #422006;
                border: 1px solid #b45309;
            }

            QLabel#system_status[platform_state="linux"] {
                color: #c4b5fd;
                background-color: #2e1065;
                border: 1px solid #7c3aed;
            }

            QLabel#system_status[platform_state="unknown"] {
                color: #cbd5e1;
                background-color: #1e293b;
                border: 1px solid #475569;
            }


            /* =================================================
               INFO
               ================================================= */

            QFrame#info_frame {
                background-color: #111c32;
                border: 1px solid #1e3a5f;
                border-radius: 9px;
            }

            QLabel#info_icon {
                color: #60a5fa;
                font-size: 18px;
                font-weight: 700;
            }

            QLabel#info_text {
                color: #94a3b8;
                font-size: 12px;
            }


            /* =================================================
               SUMMARY CARDS
               ================================================= */

            QFrame#summary_card {
                background-color: #111827;
                border: 1px solid #243044;
                border-radius: 11px;
            }

            QFrame#summary_card:hover {
                border: 1px solid #334155;
            }

            QLabel#card_heading {
                color: #64748b;
                font-size: 9px;
                font-weight: 800;
                letter-spacing: 1px;
            }

            QLabel#card_value {
                color: #f8fafc;
                font-size: 24px;
                font-weight: 750;
            }

            QLabel#card_description {
                color: #64748b;
                font-size: 10px;
            }


            /* =================================================
               SERVICE PANEL
               ================================================= */

            QFrame#service_frame {
                background-color: #111827;
                border: 1px solid #243044;
                border-radius: 12px;
            }

            QLabel#section_title {
                color: #f8fafc;
                font-size: 19px;
                font-weight: 750;
            }

            QLabel#section_description {
                color: #64748b;
                font-size: 11px;
            }


            /* =================================================
               TABLE
               ================================================= */

            QTableWidget#service_table {
                background-color: #0f172a;
                alternate-background-color: #111c2e;
                color: #e5e7eb;
                border: 1px solid #263449;
                border-radius: 8px;
                gridline-color: #263449;
                outline: none;
                font-size: 12px;
            }

            QTableWidget#service_table::item {
                background-color: #0f172a;
                color: #e5e7eb;
                border-bottom: 1px solid #1e293b;
                padding-left: 9px;
                padding-right: 9px;
            }

            QTableWidget#service_table::item:hover {
                background-color: #172033;
            }

            QHeaderView::section {
                background-color: #172033;
                color: #94a3b8;
                border: none;
                border-bottom: 1px solid #334155;
                padding: 10px 9px;
                font-size: 10px;
                font-weight: 800;
            }


            /* =================================================
               VERTICAL SCROLLBAR
               ================================================= */

            QTableWidget#service_table QScrollBar:vertical {
                background-color: #0b1120;
                width: 14px;
                margin: 2px;
                border-radius: 6px;
            }

            QTableWidget#service_table QScrollBar::handle:vertical {
                background-color: #475569;
                min-height: 40px;
                border-radius: 6px;
            }

            QTableWidget#service_table QScrollBar::handle:vertical:hover {
                background-color: #64748b;
            }

            QTableWidget#service_table QScrollBar::add-line:vertical,
            QTableWidget#service_table QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QTableWidget#service_table QScrollBar::add-page:vertical,
            QTableWidget#service_table QScrollBar::sub-page:vertical {
                background-color: transparent;
            }


            /* =================================================
               HORIZONTAL SCROLLBAR
               ================================================= */

            QTableWidget#service_table QScrollBar:horizontal {
                background-color: #0b1120;
                height: 10px;
                border-radius: 5px;
            }

            QTableWidget#service_table QScrollBar::handle:horizontal {
                background-color: #475569;
                border-radius: 5px;
                min-width: 50px;
            }

            QTableWidget#service_table QScrollBar::add-line:horizontal,
            QTableWidget#service_table QScrollBar::sub-line:horizontal {
                width: 0px;
            }


            /* =================================================
               COMMON BUTTON
               ================================================= */

            QPushButton {
                border-radius: 6px;
                padding: 5px 8px;
                font-size: 10px;
                font-weight: 700;
            }

            QPushButton:pressed {
                padding-top: 6px;
                padding-bottom: 4px;
            }


            /* =================================================
               INSTALL
               ================================================= */

            QPushButton#install_button {
                color: #a5b4fc;
                background-color: #1e1b4b;
                border: 1px solid #4338ca;
            }

            QPushButton#install_button:hover {
                background-color: #312e81;
            }


            /* =================================================
               START
               ================================================= */

            QPushButton#start_button {
                color: #6ee7b7;
                background-color: #052e1b;
                border: 1px solid #047857;
            }

            QPushButton#start_button:hover {
                background-color: #064e3b;
            }


            /* =================================================
               STOP
               ================================================= */

            QPushButton#stop_button {
                color: #fca5a5;
                background-color: #450a0a;
                border: 1px solid #b91c1c;
            }

            QPushButton#stop_button:hover {
                background-color: #7f1d1d;
            }


            /* =================================================
               RESTART
               ================================================= */

            QPushButton#restart_button {
                color: #fdba74;
                background-color: #431407;
                border: 1px solid #c2410c;
            }

            QPushButton#restart_button:hover {
                background-color: #7c2d12;
            }


            /* =================================================
               ENABLE
               ================================================= */

            QPushButton#enable_button {
                color: #86efac;
                background-color: #052e16;
                border: 1px solid #15803d;
            }

            QPushButton#enable_button:hover {
                background-color: #14532d;
            }


            /* =================================================
               DISABLE
               ================================================= */

            QPushButton#disable_button {
                color: #cbd5e1;
                background-color: #1e293b;
                border: 1px solid #475569;
            }

            QPushButton#disable_button:hover {
                background-color: #334155;
            }


            /* =================================================
               PREVIEW
               ================================================= */

            QPushButton#preview_button {
                color: #7dd3fc;
                background-color: #082f49;
                border: 1px solid #0369a1;
            }

            QPushButton#preview_button:hover {
                background-color: #0c4a6e;
            }


            /* =================================================
               REFRESH
               ================================================= */

            QPushButton#refresh_button {
                color: #cbd5e1;
                background-color: #1e293b;
                border: 1px solid #475569;
                font-size: 11px;
                padding: 7px 16px;
            }

            QPushButton#refresh_button:hover {
                background-color: #334155;
                border-color: #64748b;
            }


            /* =================================================
               PREVIEW DIALOG
               ================================================= */

            QDialog#command_preview_dialog {
                background-color: #0b1120;
            }

            QLabel#preview_title {
                color: #f8fafc;
                font-size: 21px;
                font-weight: 750;
            }

            QLabel#preview_description {
                color: #94a3b8;
                font-size: 12px;
            }

            QFrame#preview_info_frame {
                background-color: #111827;
                border: 1px solid #263449;
                border-radius: 8px;
            }

            QLabel#preview_info {
                color: #cbd5e1;
                font-size: 12px;
                font-weight: 600;
            }


            /* =================================================
               TERMINAL
               ================================================= */

            QTextEdit#command_preview_text {
                background-color: #020617;
                color: #dbeafe;
                border: 1px solid #263449;
                border-radius: 8px;
                padding: 12px;
                font-family: "Consolas",
                             "Cascadia Mono",
                             "Courier New",
                             monospace;
                font-size: 12px;
                selection-background-color: #1e3a5f;
            }


            /* =================================================
               DRY RUN
               ================================================= */

            QLabel#dry_run_label {
                color: #6ee7b7;
                background-color: #052e1b;
                border: 1px solid #047857;
                border-radius: 7px;
                padding: 8px 10px;
                font-size: 11px;
                font-weight: 700;
            }


            /* =================================================
               DIALOG BUTTON
               ================================================= */

            QDialogButtonBox QPushButton {
                color: #cbd5e1;
                background-color: #1e293b;
                border: 1px solid #475569;
                padding: 7px 18px;
                min-width: 75px;
            }

            QDialogButtonBox QPushButton:hover {
                background-color: #334155;
            }


            /* =================================================
               FOOTER
               ================================================= */

            QLabel#footer {
                color: #475569;
                font-size: 10px;
            }

            QLabel#footer_status {
                color: #34d399;
                font-size: 10px;
                font-weight: 700;
            }

            """
        )