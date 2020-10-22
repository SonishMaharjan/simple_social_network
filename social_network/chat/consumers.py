# it's like a view for normal request,
#it accepts the web socket request and process it

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # scope containls most of the information that you find in djagno's request
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        print("hello my socket")

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    #Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message_pasa',
                'message': message
            }
        )

    # Receive message from room group
    # send message to FE sockets
    def chat_message_pasa(self, event):
        message = event['message']
        # Send message to  FE WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
