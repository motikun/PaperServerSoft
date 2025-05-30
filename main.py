from gui.main_window import AppLauncher
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = AppLauncher()
    launcher.showMaximized()
    sys.exit(app.exec())