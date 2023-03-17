import requests # For API Requests
import webbrowser # For opening browser during OAuth
from flask import Flask, request # For accepting oauth
import time # to wait for oauth
from multiprocessing import Process # run things simultaneously
from guli import GuliVariable

# Exception for when the user did not authenticate
class UserDidNotAuthenticate(Exception):
    pass

class GroupMeClient:
    def __init__(self, client_id, oauth_wait_time=60, oauth_wait_till_success=True, access_token=None, app_name='GroupPy'):
        # Establish URL
        self.api_url = 'https://api.groupme.com/v3'
        self.client_id = client_id
        
        # Some Settings:
        self.oauth_wait_time = oauth_wait_time
        self.access_token = access_token
        self.app_name = app_name
        self.oauth_wait_till_success = oauth_wait_till_success

    def authenticate(self):
        """ Authenticate with GroupMe """
        webbrowser.open(f'https://oauth.groupme.com/oauth/authorize?client_id={self.client_id}')
        GuliVariable("grouppy.access_token").setValue(self.access_token)

        # Define Webserver
        html_success_page = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>{self.app_name} Authentication</title>
            </head>
            <body style="font-family:Cantarell,Sans-serif;padding-top:30px;">
                <center>
                    <h3><strong>Success!</strong></h3>
                    <h4>You may now close this window.</h4>
                </center>
            </body>
        <html>
        """
        self.flask_server = Flask(__name__)
        @self.flask_server.route('/oauth', methods=['GET'])
        def oauth():
            args = request.args
            GuliVariable("grouppy.access_token").setValue(args.get('access_token'))
            print(f'self.access_token = {self.access_token}')
            return html_success_page
        
        # Start Webserver
        webserver = Process(target=self.flask_server.run, kwargs=dict(host='127.0.0.1', port='8089'))
        webserver.start()

        
        # Wait for oauth to complete, or to be told it's done.
        if self.oauth_wait_till_success:
            #count = 0
            while GuliVariable("grouppy.access_token").get() == None:
                time.sleep(1)
                #count += 1
                #print(f'[{count}]: Not authenticated yet...')
                #print(f'[{count}]: Access Token: {self.access_token}')
            print('Authentication completed!')
        elif self.oauth_wait_time <= 0:
            self.oauth_wait_time_remaining = self.oauth_wait_time
            for i in range(self.oauth_wait_time):
                time.sleep(1)
                self.oauth_wait_time_remaining = self.oauth_wait_time - i
        else:
            self.authenticate_confirm = False
            while not self.authenticate_confirm:
                time.sleep(1)

        # Check if authentication was completed
        if GuliVariable("grouppy.access_token").get() == None:
            if self.oauth_wait_till_success:
                message = 'User appeared to finish authentication, but didnt! (This should never happen)'
            elif self.oauth_wait_time <= 0:
                message = 'User did not finish authentication within the timeout.'
            else:
                message = 'User did not finish authentication'
            webserver.kill()
            raise UserDidNotAuthenticate('User did not finish authentication within the timeout.')
            return False

        # Terminate webserver, we don't need it anymore!
        webserver.kill()
        webserver.join()

        # Save token as variable
        self.access_token = GuliVariable("grouppy.access_token").get()
        GuliVariable("grouppy.access_token").setValue(None) # anc clear for security
    
    def authenticate_confirm(self):
        """ Confirm Authentication Instead of Waiting for timeout """
        self.authenticate_confirm = True
    
    def get_groups(self, entries=200, page=1):
        """ Fetch Groups from the API """
        parameters = { 'access_token' : self.access_token, 'per_page' : f'{entries}', 'page' : f'{page}'}
        response_raw = requests.get(f'{self.api_url}/groups', params=parameters)
        response = response_raw.json()
        print('RESPONSE: \n' + str(response['response']))
        pass
        self.groups_raw = response['response']
        self.group_ids = []
        self.groups = {}
        for group in self.groups:
            self.group_ids.append(self.groups_raw[group['id']])
            group_id = group['id']
            print(f'ID: { group_id }\nCONTENT: {group}')
            self.groups[group['id']] = group

        
