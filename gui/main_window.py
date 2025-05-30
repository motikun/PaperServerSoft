from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QMessageBox, QListWidget, QSizePolicy, QHBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt
from create import CreateServerDialog
from src.start_server import connect_selection_signal, start_server, get_server_dir
from load_json import load_servers
from src.server_config import server_config
import sys
import json
import os

class AppLauncher:
    def __init__(self):
        self.server_list = None

    def launch_app(self):
        json_load = load_servers()
        app = QApplication(sys.argv)
        window = QWidget()
        window.setWindowTitle("ランチャー")

        #左側レイアウト
        left_layout = QVBoxLayout()

        self.server_list = QListWidget()
        self.server_list.setFixedWidth(300)
        self.server_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        for item in json_load:
            self.server_list.addItem(f"{item['name']}")
        connect_selection_signal(self.server_list)

        create_button = QPushButton("サーバーを作成")
        create_button.setFixedSize(300, 50)
        create_button.clicked.connect(lambda: CreateServerDialog().exec())

        left_layout.addWidget(QLabel("サーバー一覧："))
        left_layout.addWidget(self.server_list)
        left_layout.addWidget(create_button)

        #右側レイアウト
        right_layout = QVBoxLayout()

        #------設定とか------
        settings_layout = QHBoxLayout()

        start_button = QPushButton("起動")
        start_button.setFixedSize(200, 50)
        start_button.clicked.connect(self.run_server)

        stop_button = QPushButton("停止")
        stop_button.setFixedSize(200, 50)

        settings_button = QPushButton("サーバー設定")
        settings_button.setFixedSize(200, 50)
        settings_button.clicked.connect(self.handle_server_config)

        settings_layout.addStretch()
        settings_layout.addWidget(start_button)
        settings_layout.addWidget(stop_button)
        settings_layout.addWidget(settings_button)
        #------ここまで------

        log_text = QTextEdit()
        log_text.setReadOnly(True)
        log_text.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        right_layout.addStretch()
        right_layout.addLayout(settings_layout)
        right_layout.addWidget(log_text)

        #レイアウトまとめ
        main_layout = QHBoxLayout()

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        window.setLayout(main_layout)
        window.showMaximized()

        sys.exit(app.exec())

    def handle_server_config(self):
        server_config(self)

    def run_server(self):
        selected_server_dir = get_server_dir(self.server_list)
        start_server(selected_server_dir)