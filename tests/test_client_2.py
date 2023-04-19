import datetime

from grouppy import GroupMeClient, GroupMeListener

print(f'Welcome to GroupPy Manual Testing!')

client = GroupMeClient(input('> Paste Your Access Token: '), oauth_complete=True)

print(f'\nFetching Groups...')
for group in client.get_groups():
    print(f'> {group["name"]}\n  {group["group_id"]}')

print(f'\nTesting message sending...')
group = input(f'> Paste a Group ID to send a message in: ')
message = input(f'> Type your message: ')
print(f'> Sending Message "{message}"...')

client.send_message(group, message)

print(f'\nTesting Complete!')

