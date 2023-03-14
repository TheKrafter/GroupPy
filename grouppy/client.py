from rest3client import RESTclient # For API Requests
import webbrowser # For opening browser during OAuth
from flask import Flask, request # For accepting oauth
import time # to wait for oauth
from multiprocessing import Process

class GroupMeClient():
    def __init__(client_id, oauth_wait_time=30, access_token=None):
        # Establish URL
        self.api = RESTclient('https://api.groupme.com/v3')
        self.client_id = client_id
        
        # Some Settings:
        self.oauth_wait_time = oauth_wait_time
        self.access_token = access_token

    def authenticate(self):
        """ Authenticate with GroupMe """
        webbrowser.open(f'https://oauth.groupme.com/oauth/authorize?client_id={self.client_id}')

        webserver = Process(target=app.run, kwargs=dict(host='0.0.0.0', port='8089'))
        webserver.start()

        @app.route('/oauth', methods=['GET'])
        def oauth():
            args = request.args
            self.access_token = args.get('access_token')
        
        # Wait for oauth to complete, or to be told it's done.
        if self.oauth_wait_time >= 0:
            self.oauth_wait_time_remaining = self.oauth_wait_time
            for i in range(self.oauth_wait_time):
                time.sleep(1)
                self.oauth_wait_time_remaining = self.oauth_wait_time - i
            if self.access_token == None:
                raise DidNotAuthenticate
        else:
            self.authenticate_confirm = False
            while not self.authenticate_confirm:
                time.sleep(1)
            if self.access_token == None:
                raise DidNotAuthenticate

        webserver.terminate()

        # Set new self.api with new token
        # Save token as variable
    
    def authenticate_confirm(self):
        """ Confirm Authentication Instead of Waiting for timeout """
        self.authenticate_confirm = True

    
    def get_groups(self):
        """ Fetch Groups from the API """
        response = self.api.get('/groups', per_page='200')
        self.groups = response['response']
        self.group_ids = []
        for itm in self.groups:
            self.group_ids.append(self.groups[itm]['id'])
        
