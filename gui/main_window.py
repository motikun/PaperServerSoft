from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QMessageBox, QListWidget, QSizePolicy, QHBoxLayout, QTextEdit,
    QLineEdit
)
from PyQt6.QtCore import Qt
from create import CreateServerDialog
from src.start_server import connect_selection_signal, get_server_dir, ServerWorker
from src.plugin_list import list_plugins
from gui.plugin_config import open_plugin_config
from load_json import load_servers
from src.server_config import server_config
from src.delete_server import delete_server
import sys
import os

class AppLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.server_list = None
        self.log_text = None
        self.worker = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ランチャー")

        json_load = load_servers()

        # --- 左側レイアウト ---
        left_layout = QVBoxLayout()

        self.server_list = QListWidget()
        self.server_list.setFixedWidth(300)
        self.server_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        for item in json_load:
            self.server_list.addItem(item['name'])

        connect_selection_signal(self.server_list)
        self.server_list.itemSelectionChanged.connect(self.update_plugin_list)

        create_button = QPushButton("サーバーを作成")
        create_button.setFixedSize(300, 50)
        create_button.clicked.connect(self.open_create_dialog)

        left_layout.addWidget(QLabel("サーバー一覧："))
        left_layout.addWidget(self.server_list)
        left_layout.addWidget(create_button)

        # --- 右側レイアウト ---
        right_layout = QVBoxLayout()

        settings_layout = QHBoxLayout()

        self.plugins_list_widget = QListWidget()
        self.plugins_list_widget.setFixedHeight(200)
        self.plugins_list_widget.itemDoubleClicked.connect(lambda item: self.handle_plugin_config(item, self.server_list, parent=self))

        start_button = QPushButton("起動")
        start_button.setFixedSize(200, 50)
        start_button.clicked.connect(self.run_server)

        stop_button = QPushButton("停止")
        stop_button.setFixedSize(200, 50)

        settings_button = QPushButton("サーバー設定")
        settings_button.setFixedSize(200, 50)
        settings_button.clicked.connect(self.handle_server_config)

        delete_button = QPushButton("このサーバーを削除")
        delete_button.setFixedSize(200, 50)
        delete_button.clicked.connect(self.handle_delete_server)

        settings_layout.addStretch()
        settings_layout.addWidget(start_button)
        settings_layout.addWidget(stop_button)
        settings_layout.addWidget(settings_button)
        settings_layout.addWidget(delete_button)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self.server_command = QLineEdit()
        self.server_command.setFixedHeight(30)
        self.server_command.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        right_layout.addWidget(QLabel("プラグイン一覧:"))
        right_layout.addWidget(self.plugins_list_widget)
        right_layout.addLayout(settings_layout)
        right_layout.addWidget(self.log_text)
        right_layout.addWidget(self.server_command)

        # --- メインレイアウト ---
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def update_plugin_list(self):
        selected_server_dir = get_server_dir(self.server_list)
        list_plugins(selected_server_dir, self.plugins_list_widget)

    def handle_plugin_config(self, item, server_list, parent=None):
        selected_server_dir = get_server_dir(server_list)
        open_plugin_config(item, selected_server_dir, parent=parent)

    def run_server(self):
        selected_server_dir = get_server_dir(self.server_list)
        if not selected_server_dir:
            QMessageBox.warning(self, "エラー", "サーバーが選択されていません")
            return

        self.worker = ServerWorker(selected_server_dir)
        self.worker.server_log.connect(self.append_log)
        self.worker.start()

    def append_log(self, text):
        self.log_text.append(text)

    def handle_server_config(self):
        server_config(self, parent=self)

    def handle_delete_server(self):
        delete_server(self, parent=self)

    def refresh_server_list(self):
        self.server_list.clear()
        for item in load_servers():
            self.server_list.addItem(item["name"])

    def open_create_dialog(self):
        dialog = CreateServerDialog()
        dialog.server_created.connect(self.refresh_server_list)
        dialog.exec()

# アプリ起動用コード
if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = AppLauncher()
    launcher.showMaximized()
    sys.exit(app.exec())