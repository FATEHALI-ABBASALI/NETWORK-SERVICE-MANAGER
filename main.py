import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


# =========================================================
# Application Entry Point
# =========================================================


def main() -> None:
    """
    Start the Network Service Manager application.
    """

    app = QApplication(sys.argv)

    # -----------------------------------------------------
    # Application Metadata
    # -----------------------------------------------------

    app.setApplicationName(
        "Network Service Manager"
    )

    app.setApplicationVersion(
        "1.0.0"
    )

    # -----------------------------------------------------
    # Main Window
    # -----------------------------------------------------

    window = MainWindow()

    window.show()

    # -----------------------------------------------------
    # Qt Event Loop
    # -----------------------------------------------------

    sys.exit(
        app.exec()
    )


# =========================================================
# Script Entry
# =========================================================


if __name__ == "__main__":
    main()