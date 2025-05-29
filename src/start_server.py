import subprocess

def connect_selection_signal(server_list):
    server_list.itemSelectionChanged.connect(lambda: start_server(server_list))

def start_server(server_list):
    selected_servers = server_list.selectedItems()
    for selected_server in selected_servers:
        print(selected_server.text())
