import os
import stat
import json
import shutil
from PyQt6.QtWidgets import QMessageBox
from load_json import load_servers

def delete_server(launcher, parent=None):
    servers = load_servers()
    selected_servers = launcher.server_list.selectedItems()
    
    if not selected_servers:
        QMessageBox.warning(parent, "警告", "サーバーを選択してください")
        return

    selected_server_name = selected_servers[0].text()
    selected_server_dir = next((item['dir'] for item in servers if item['name'] == selected_server_name), None)

    if not selected_server_dir:
        QMessageBox.critical(parent, "エラー", "選択されたサーバーのディレクトリが見つかりません。")
        return

    try:
        updated_servers = [entry for entry in servers if not (entry["name"] == selected_server_name and entry["dir"] == selected_server_dir)]
        
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        json_path = os.path.join(parent_dir, 'servers.json')

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(updated_servers, f, ensure_ascii=False, indent=2)

        if os.path.exists(selected_server_dir):
            if os.path.isdir(selected_server_dir):
                shutil.rmtree(selected_server_dir)
            else:
                os.chmod(selected_server_dir, stat.S_IWRITE)
                os.remove(selected_server_dir)

        QMessageBox.information(parent, "成功", f"{selected_server_name} を削除しました。")

    except PermissionError:
        QMessageBox.critical(parent, "エラー", "Permissionエラーにより削除できませんでした")
    except Exception as e:
        QMessageBox.critical(parent, "エラー", f"サーバーを削除できませんでした。\n{e}")
