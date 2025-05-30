from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QCheckBox, QPushButton, QMessageBox,
    QScrollArea, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
import os
from load_json import load_servers

def server_config(launcher, parent=None):
    load_json = load_servers()
    selected_servers = launcher.server_list.selectedItems()

    if not selected_servers:
        QMessageBox.warning(parent, "警告", "サーバーを選択してください。")
        return

    selected_server_name = selected_servers[0].text()
    selected_server_dir = next((item['dir'] for item in load_json if item['name'] == selected_server_name), None)

    server_path = os.path.join(selected_server_dir, "server.properties")
    if not os.path.exists(server_path):
        QMessageBox.critical(parent, "エラー", "設定ファイルが存在しません。\n一度サーバーを起動し生成してください")
        return

    server_properties = load_properties(server_path)

    # ---------- UI 設定 ----------
    window = QWidget()
    window.setWindowTitle("サーバー設定")

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)

    scroll_content = QWidget()
    main_layout = QVBoxLayout(scroll_content)

    input_widgets = {}

    dropdown_options = {
        "difficulty": ["peaceful", "easy", "normal", "hard"],
        "gamemode": ["0", "1", "2", "3", "survival", "creative", "adventure", "spectator"],
        "level-type": ["DEFAULT", "FLAT", "LARGEBIOMES", "AMPLIFIED", "CUSTOMIZED"]
    }

    numeric_keys = [
        "max-players", "view-distance", "server-port", "max-world-size",
        "max-build-height", "player-idle-timeout", "network-compression-threshold",
        "op-permission-level"
    ]

    for key, value in server_properties.items():
        row_layout = QHBoxLayout()
        label = QLabel(key)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        widget = None
        if value.lower() in ["true", "false"]:
            checkbox = QCheckBox()
            checkbox.setChecked(value.lower() == "true")
            widget = checkbox
        elif key in dropdown_options:
            combo = QComboBox()
            combo.addItems(dropdown_options[key])
            combo.setCurrentText(value)
            widget = combo
        elif key in numeric_keys:
            line_edit = QLineEdit(value)
            line_edit.setValidator(QIntValidator())
            widget = line_edit
        else:
            line_edit = QLineEdit(value)
            widget = line_edit

        input_widgets[key] = widget

        row_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
        row_layout.addStretch()
        row_layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(row_layout)

    save_button = QPushButton("保存")
    main_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignRight)

    def save_config():
        with open(server_path, "w", encoding="utf-8") as f:
            for key, widget in input_widgets.items():
                if isinstance(widget, QCheckBox):
                    value = "true" if widget.isChecked() else "false"
                elif isinstance(widget, QComboBox):
                    value = widget.currentText()
                elif isinstance(widget, QLineEdit):
                    value = widget.text()
                else:
                    continue
                f.write(f"{key}={value}\n")

        QMessageBox.information(window, "成功", "設定を保存しました")

    save_button.clicked.connect(save_config)

    scroll_area.setWidget(scroll_content)

    final_layout = QVBoxLayout(window)
    final_layout.addWidget(scroll_area)

    launcher.config_window = window
    window.resize(600, 600)
    window.show()

def load_properties(filepath):
    props = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() == "" or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.strip().split("=", 1)
                props[key] = value
    return props