from grouppy import client

token = input('GroupMe Client ID: ')

client  = GroupMeClient(token)

client.authenticate()

client.get_groups()

