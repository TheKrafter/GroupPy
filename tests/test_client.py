from grouppy import GroupMeClient

with open('./client_id.txt', 'r') as client_txt:
    token = client_txt.read().replace('\n', '')

print(f'\nGroupMe Client ID retrieved from file.')

client  = GroupMeClient(token, oauth_wait_time=30)

print(f'You have {client.oauth_wait_time} seconds to authenticate!')

client.authenticate()

client.get_groups()

print(f'Groups: \n {client.groups}')