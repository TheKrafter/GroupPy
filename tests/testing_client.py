import datetime

from grouppy import GroupMeClient

print(f'Welcome to GroupPy Manual Testing!')

token = input('> Paste Your Access Token: ')
client = GroupMeClient(token, oauth_complete=True)

print(f'\nFetching Groups...')
for group in client.get_groups():
    print(f'> {group["name"]}\n  {group["group_id"]}')

print(f'\nTesting message sending and fetching...')
group = input(f'> Paste a Group ID to send a message in: ')
for message in reversed(client.get_messages(group, limit=15)["messages"]):
    print(f'[{datetime.datetime.fromtimestamp(message["created_at"]).strftime("%Y-%m-%d %H:%M:%S")}] {message["name"]} : {message["text"]}')
message = input(f'> Type your message: ')
print(f'> Sending Message "{message}"...')

client.send_message(group, message)

print(f'\nTesting Complete!')

