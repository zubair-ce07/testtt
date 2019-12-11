from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
        if self.scope['url_route']['kwargs']['username'] == 'dummy':
            self.close()
        else:    
            async_to_sync(self.channel_layer.group_add)(
                'social_app',
                self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        print("Closed websocket with code: ", close_code)
        async_to_sync(self.channel_layer.group_discard)(
            'social_app',
            self.channel_name
        )
        self.close()

    def send_notification(self, event):
        event['type'] = event['action']
        self.send_json(event)

    def CREATE_COMMENT_FULFILLED(self, event):
        self.send_json(event)

    def UPDATE_COMMENT_FULFILLED(self, event):
        self.send_json(event)

    def DELETE_COMMENT_FULFILLED(self, event):
        self.send_json(event)

    def CREATE_POST_FULFILLED(self, event):
        self.send_json(event)

    def UPDATE_POST_FULFILLED(self, event):
        self.send_json(event)

    def DELETE_POST_FULFILLED(self, event):
        self.send_json(event)
