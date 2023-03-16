from grouppy import GroupMeClient

token = input('\nGroupMe Client ID: ')

client  = GroupMeClient(token, oauth_wait_time=30)

print(f'You have {client.oauth_wait_time} seconds to authenticate!')

client.authenticate()

client.get_groups()

print(f'Groups: \n {self.groups}')