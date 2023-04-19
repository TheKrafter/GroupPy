import datetime

from grouppy import GroupMeListener

print(f'Welcome to GroupPy Listener Manual Testing')

token = input('> Paste your access token: ')
listener = GroupMeListener(token)

@listener.on_message
def handle_message(listener, data):
    print(data)
    pass

listener.connect()
