from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from create import CreateServerDialog
import sys

def launch_app():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("ランチャー")

    layout = QVBoxLayout()
    button = QPushButton("PaperMCサーバー作成")
    button.clicked.connect(lambda: CreateServerDialog().exec())
    layout.addWidget(button)

    window.setLayout(layout)
    window.showMaximized()

    sys.exit(app.exec())
