from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from create import CreateServerDialog
import sys
import json
import os

def launch_app():
    layout = QVBoxLayout()
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    json_path = os.path.join(parent_dir, 'servers.json')

    if not os.path.exists(json_path):
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
            
    json_open = open(json_path, 'r', encoding='utf-8')
    json_load = json.load(json_open)

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("ランチャー")

    button = QPushButton("PaperMCサーバー作成")
    button.setFixedSize(300, 100)
    button.clicked.connect(lambda: CreateServerDialog().exec())

    for item in json_load:
        label = QLabel(f"{item['dir']}")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

    layout.addStretch()
    layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addStretch()

    window.setLayout(layout)
    window.showMaximized()

    sys.exit(app.exec())
