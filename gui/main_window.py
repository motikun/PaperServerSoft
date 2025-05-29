from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from create import CreateServerDialog
import sys

def launch_app():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("ランチャー")

    button = QPushButton("PaperMCサーバー作成")
    button.setFixedSize(300, 100)
    button.clicked.connect(lambda: CreateServerDialog().exec())

    layout = QVBoxLayout()
    layout.addStretch()
    layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addStretch()

    window.setLayout(layout)
    window.showMaximized()

    sys.exit(app.exec())
