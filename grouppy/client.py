from rest3client import RESTclient # For API Requests
import webbrowser # For opening browser during OAuth
from flask import Flask, request

class GroupMeClient():
    def __init__(client_id):
        # Establish URL
        self.api = RESTclient('https://api.groupme.com/v3')
        self.client_id = client_id

    def authenticate(self):
        """ Authenticate with GroupMe """
        webbrowser.open(f'https://oauth.groupme.com/oauth/authorize?client_id={self.client_id}')

        @app.route('/oauth', methods=['GET'])
        def search():
            args = request.args
            name = args.get('access_token')
            
        
        # Store URL
        # Set new self.api with new token
        # Save token as variable

    
    def get_groups(self):
        """ Fetch Groups from the API """
        response = self.api.get('/groups', per_page='200')
        self.groups = response['response']
        self.group_ids = []
        for itm in self.groups:
            self.group_ids.append(self.groups[itm]['id'])
        
