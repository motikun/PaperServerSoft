from load_json import load_servers
import subprocess

def connect_selection_signal(server_list):
    server_list.itemSelectionChanged.connect(lambda: get_server_dir(server_list))

def get_server_dir(server_list):
    json_load = load_servers()
    selected_servers = server_list.selectedItems()
    for selected_server in selected_servers:
        selected_server_name = selected_server.text()
        selected_server_dir = None
        for item in json_load:
            if item['name'] == selected_server_name:
                return item['dir']

def start_server(selected_server_dir):
    try:
        print(f"{selected_server_dir}/start.bat")
        subprocess.run(["cmd.exe", "/c", f"{selected_server_dir}/start.bat"], cwd=selected_server_dir)
    except Exception as e:
        print(f"実行エラー: {e}")