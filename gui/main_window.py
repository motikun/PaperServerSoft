from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QMessageBox, QListWidget, QSizePolicy, QHBoxLayout
)
from PyQt6.QtCore import Qt
from create import CreateServerDialog
import sys
import json
import os

def launch_app():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    json_path = os.path.join(parent_dir, 'servers.json')

    if not os.path.exists(json_path):
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    with open(json_path, 'r', encoding='utf-8') as json_open:
        json_load = json.load(json_open)

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("ランチャー")

    left_layout = QVBoxLayout()

    server_list = QListWidget()
    server_list.setFixedWidth(300)
    server_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    for item in json_load:
        server_list.addItem(f"{item['dir']}")

    create_button = QPushButton("サーバーを作成")
    create_button.setFixedSize(300, 50)
    create_button.clicked.connect(lambda: CreateServerDialog().exec())

    left_layout.addWidget(QLabel("サーバー一覧："))
    left_layout.addWidget(server_list)
    left_layout.addWidget(create_button)

    window.setLayout(left_layout)
    window.showMaximized()

    sys.exit(app.exec())