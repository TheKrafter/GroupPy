from grouppy import GroupMeClient

test_oauth = False

if test_oauth:
    with open('./client_id.txt', 'r') as client_txt:
        token = client_txt.read().replace('\n', '')
    oauth_complete = False
else:
    with open('./access_token.txt', 'r') as access_token_txt:
        token = access_token_txt.read().replace('\n', '')
    oauth_complete = True

print(f'\nGroupMe Client ID retrieved from file.')


client  = GroupMeClient(token, oauth_complete=oauth_complete)

if test_oauth:
    client.authenticate()

client.get_groups()

print(f'Groups: \n {client.groups}')

assert 'grouppy testing 3243' in str(client.groups), 'Should be in testing guild'

with open('./result.txt', 'a') as result_txt:
    result_txt.write(str(client.groups) + '\n')