from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QCheckBox, QPushButton, QMessageBox
)
from load_json import load_servers

def server_config(launcher, parent=None):
    load_json = load_servers()
    selected_servers = launcher.server_list.selectedItems()

    if not selected_servers:
        QMessageBox.warning(parent, "警告", "サーバーを選択してください。")
        return

    for selected_server in selected_servers:
        selected_server_name = selected_server.text()
        selected_server_dir = None
        for item in load_json:
            if item['name'] == selected_server_name:
                selected_server_dir = item['dir']
                break

    server_path = selected_server_dir + "/server.properties"
    server_properties = load_properties(server_path)

    window = QWidget()
    window.setWindowTitle("サーバー設定")
    main_layout = QVBoxLayout()

    input_widgets = {}

    for key, value in server_properties.items():
        row_layout = QHBoxLayout()
        label = QLabel(key)

        if value.lower() in ["true", "false"]:
            checkbox = QCheckBox()
            checkbox.setChecked(value.lower() == "true")
            input_widgets[key] = checkbox
            row_layout.addWidget(label)
            row_layout.addWidget(checkbox)
        else:
            line_edit = QLineEdit(value)
            input_widgets[key] = line_edit
            row_layout.addWidget(label)
            row_layout.addWidget(line_edit)

        main_layout.addLayout(row_layout)

    save_button = QPushButton("保存")
    main_layout.addWidget(save_button)

    def save_config():
        with open(server_path, "w", encoding="utf-8") as f:
            for key, widget in input_widgets.items():
                if isinstance(widget, QCheckBox):
                    value = "true" if widget.isChecked() else "false"
                elif isinstance(widget, QLineEdit):
                    value = widget.text()
                else:
                    continue
                f.write(f"{key}={value}\n")

        QMessageBox.information(window, "成功", "設定を保存しました")

    save_button.clicked.connect(save_config)

    window.setLayout(main_layout)
    launcher.config_window = window
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