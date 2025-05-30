from load_json import load_servers
from PyQt6.QtCore import pyqtSignal, QThread
import subprocess

class ServerWorker(QThread):
    server_log = pyqtSignal(str)

    def __init__(self, selected_server_dir):
        super().__init__()
        self.selected_server_dir = selected_server_dir

    def run(self):
        try:
            process = subprocess.Popen(
                ["cmd.exe", "/c", f"{self.selected_server_dir}/start.bat"], 
                cwd=self.selected_server_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                self.server_log.emit(line.strip())

            process.stdout.close()
            process.wait()

        except Exception as e:
            self.server_log.emit(f"実行エラー: {e}")

def connect_selection_signal(server_list):
    server_list.itemSelectionChanged.connect(lambda: get_server_dir(server_list))

def get_server_dir(server_list):
    json_load = load_servers()
    selected_servers = server_list.selectedItems()
    for selected_server in selected_servers:
        selected_server_name = selected_server.text()
        for item in json_load:
            if item['name'] == selected_server_name:
                return item['dir']
    return None