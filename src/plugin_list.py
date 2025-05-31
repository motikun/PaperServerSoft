import os
from PyQt6.QtWidgets import QListWidget

def list_plugins(selected_server_dir: str, plugins_list_widget: QListWidget):
    # クリアして再読み込みできるように
    plugins_list_widget.clear()

    plugins_dir = os.path.join(selected_server_dir, "plugins")

    if not os.path.exists(plugins_dir):
        plugins_list_widget.addItem("pluginsフォルダが存在しません")
        return

    plugin_files = [f for f in os.listdir(plugins_dir) if f.endswith(".jar")]

    if not plugin_files:
        plugins_list_widget.addItem("プラグインが見つかりません")
        return

    for plugin in plugin_files:
        plugins_list_widget.addItem(plugin)
