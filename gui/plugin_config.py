import os
import zipfile
import yaml
from PyQt6.QtWidgets import QMessageBox, QTextEdit, QDialog, QVBoxLayout

def get_plugin_folder_name_from_jar(jar_path):
    try:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            with jar.open('plugin.yml') as plugin_yml_file:
                data = yaml.safe_load(plugin_yml_file)
                return data.get('name')  # plugin.ymlのnameがフォルダ名
    except Exception as e:
        print(f"エラー: {e}")
        return None

def open_plugin_config(item, selected_server_dir, parent=None):
    plugin_jar_name = item.text()  # 例: GSit-2.3.3.jar
    plugin_jar_path = os.path.join(selected_server_dir, "plugins", plugin_jar_name)

    if not os.path.isfile(plugin_jar_path):
        QMessageBox.warning(parent, "エラー", f"Jarファイルが見つかりません: {plugin_jar_path}")
        return

    plugin_folder_name = get_plugin_folder_name_from_jar(plugin_jar_path)
    if not plugin_folder_name:
        QMessageBox.warning(parent, "エラー", "plugin.yml からプラグイン名を取得できませんでした。")
        return

    plugin_folder_path = os.path.join(selected_server_dir, "plugins", plugin_folder_name)
    config_path = os.path.join(plugin_folder_path, "config.yml")

    if not os.path.isdir(plugin_folder_path):
        QMessageBox.warning(parent, "エラー", f"プラグインフォルダが見つかりません: {plugin_folder_path}")
        return

    if not os.path.isfile(config_path):
        QMessageBox.warning(parent, "エラー", f"config.yml が見つかりません: {config_path}")
        return

    # ファイル内容読み取り
    with open(config_path, "r", encoding="utf-8") as f:
        config_text = f.read()

    # テキスト表示用ダイアログ
    dialog = QDialog(parent)
    dialog.setWindowTitle(f"{plugin_folder_name} の config.yml")
    layout = QVBoxLayout()
    text_edit = QTextEdit()
    text_edit.setText(config_text)
    text_edit.setReadOnly(False)
    layout.addWidget(text_edit)
    dialog.setLayout(layout)
    dialog.resize(600, 400)
    dialog.exec()
