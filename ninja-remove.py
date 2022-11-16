import json
import os
import os.path

CONFIG_PATH = os.path.expanduser('~/.config/ninja-dev-sync.json')

def load_config():
    print('Loading configuration...')
    with open(CONFIG_PATH, 'r') as config:
        return json.load(config)

def save_config(data):
    print('Saving configuration...')
    with open(CONFIG_PATH, 'w') as config:
        json.dump(data, config, indent=4)

def print_workspaces(data):
    workspaces = data['Workspaces']
    print(f'Workspaces ({len(workspaces)}):')
    for index, workspace in enumerate(workspaces):
        local_sync = workspace['LocalSync']
        print(f'{str(index+1).ljust(4)} - {local_sync}')

def get_user_selection(data):
    workspaces = data['Workspaces']
    user_input = input(f'Delete workspace (1-{len(workspaces)})? ')
    user_selection = int(user_input) - 1
    if user_selection < 0 or user_selection >= len(workspaces):
        raise RuntimeError('Invalid user selection')
    return user_selection

def remove_config(data, user_selection):
    print('Removing workspace from configuration...')
    del data['Workspaces'][user_selection]

def execute_command(command):
    if input('Can I execute "{command}" (y/n)? ') == 'y':
        os.system(command)

def remove_local(data, user_selection):
    print('Removing local workspace...')
    local_sync = data['Workspaces'][user_selection]['LocalSync']
    execute_command(f'rm -rf {local_sync}')

def remove_remote(data, user_selection):
    print('Removing remote workspace...')
    workspace = data['Workspaces'][user_selection]
    remote_host = workspace['RemoteHost']
    remote_sync = workspace['RemoteSync']
    remote_command = f'rm -rf {remote_sync}'
    execute_command(f'ssh {remote_host} "{remote_command}"')

def main():
    data = load_config()
    user_selection = get_user_selection(data)
    remove_local(data, user_selection)
    remove_remote(data, user_selection)
    remove_config(data, user_selection)
    print('Workspace removed.')

if __name__ == '__main__':
    main()
