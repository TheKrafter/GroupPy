

class GroupMeListener:
    def __init__(self, access_token):
        self.access_token = access_token
        self.ws = None
    
    def connect(self):
        url = f"wss://push.groupme.com/faye?token={self.access_token}&user_id={self.user_id}"
        self.ws = websocket.WebSocketApp(url, on_message=self.on_message)
        self.ws.run_forever()
    
    def on_message(self, function):
        """ On Message Event. Called when a message is recieved through the websocket. """
        data = json.loads(message)
        if data["channel"] == "/meta/connect":
            if data["successful"]:
                print("Connected to GroupMe WebSocket API")
        elif data["channel"].startswith("/meta/"):
            pass
        else:
            # Handle incoming message, reaction, or group data
            function(data)