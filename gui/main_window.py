from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from create import CreateServerDialog
import sys
import json
import os

def launch_app():
    layout = QVBoxLayout()
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    json_path = os.path.join(parent_dir, 'servers.json')
    json_open = open(json_path, 'r', encoding='utf-8')
    json_load = json.load(json_open)

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("ランチャー")

    button = QPushButton("PaperMCサーバー作成")
    button.setFixedSize(300, 100)
    button.clicked.connect(lambda: CreateServerDialog().exec())

    for item in json_load:
        label = QLabel(f"{item["dir"]}")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

    layout.addStretch()
    layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addStretch()

    window.setLayout(layout)
    window.showMaximized()

    sys.exit(app.exec())
