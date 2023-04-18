import requests
import webbrowser
import json
import websocket
from flask import Flask, request
import time
from multiprocessing import Process
from guli import GuliVariable

# Exceptions
class UserDidNotAuthenticate(Exception):
    pass # if user authentication failed or timed out
class InvalidResponse(Exception):
    pass # if api response is invalid

class GroupMeClient:
    def __init__(self, token, oauth_complete=False, oauth_wait_time=60, oauth_wait_till_success=True, app_name='GroupPy'):
        # Establish URL
        self.api_url = 'https://api.groupme.com/v3'

        # Token Info
        if oauth_complete:
            self.access_token = token
            self.client_id = None
        else:
            self.client_id = token
            self.access_token = None
        
        # Some Settings:
        self.oauth_wait_time = oauth_wait_time
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
                message = 'User appeared to finish authentication, but didn\'t! (This should never happen)'
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
        GuliVariable("grouppy.access_token").setValue(None) # and clear for security
    
    def authenticate_confirm(self):
        """ Confirm Authentication Instead of Waiting for timeout """
        self.authenticate_confirm = True
    
    def get_groups(self, entries=50, page=1):
        """ Fetch Groups from the API """
        parameters = { 
            'per_page' : f'{entries}',
            'page' : f'{page}'
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Access-Token': self.access_token
        }
        response = requests.get(f'{self.api_url}/groups', params=parameters, headers=headers)
        if response.status_code != 200:
            # Error fetching groups!
            return []
        else:
            data = response.json()
            return data.get('response', [])

    def create_group(self, name, description=None, image_url=None):
        """ Create a new Group """
        url = f'{self.api_url}/groups'
        data = {
            'name': name,
            'description': description,
            'image_url': image_url
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Access-Token': self.access_token
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 201:
            print(f'Error creating group: {response.content}')
            return False
        else:
            data = response.json()
            print(f'Group "{data.get("name")}" created successfully')  
            return True

    def get_messages(self, group_id, limit=100):
        """ Get messages from a group"""
        url = f'{self.api_url}/groups/{group_id}/messages'
        params = {
            'limit': limit,
            'token': self.access_token
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f'Error fetching messages: {response.content}')
            return []
        else:
            data = response.json()
            return data.get('response', [])
    
    def react_to_message(self, group_id, message_id, reaction_type):
        url = f'{self.api_url}/groups/{group_id}/messages/{message_id}/like'
        data = {
            'type': reaction_type
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Access-Token': self.access_token
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            print(f'Error reacting to message: {response.content}')
            return False
        else:
            print('Reaction added successfully')
            return True

class GroupMeListener:
    def __init__(self, access_token):
        self.access_token = access_token
        self.ws = None
    
    def connect(self):
        url = f"wss://push.groupme.com/faye?token={self.access_token}&user_id={self.user_id}"
        self.ws = websocket.WebSocketApp(url, on_message=self.on_message)
        self.ws.run_forever()
    
    def on_message(self, ws, message):
        data = json.loads(message)
        if data["channel"] == "/meta/connect":
            if data["successful"]:
                print("Connected to GroupMe WebSocket API")
        elif data["channel"].startswith("/meta/"):
            pass
        else:
            # Handle incoming message, reaction, or group data
            return data

    
