from load_json import load_servers
import subprocess

def connect_selection_signal(server_list):
    server_list.itemSelectionChanged.connect(lambda: start_server(server_list))

def start_server(server_list):
    json_load = load_servers()
    selected_servers = server_list.selectedItems()
    for selected_server in selected_servers:
        selected_server_name = selected_server.text()
        selected_server_dir = None
        for item in json_load:
            if item['name'] == selected_server_name:
                selected_server_dir = item['dir']
                break
        print(selected_server_dir)
