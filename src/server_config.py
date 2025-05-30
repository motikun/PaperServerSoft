from load_json import load_servers

def server_config(launcher):
    json_load = load_servers()
    selected_servers = launcher.server_list.selectedItems()
    for selected_server in selected_servers:
        selected_server_name = selected_server.text()
        selected_server_dir = None
        for item in json_load:
            if item['name'] == selected_server_name:
                selected_server_dir = item['dir']
                break
        print(selected_server_dir)