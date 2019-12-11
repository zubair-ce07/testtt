from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
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

        if not hasattr(self, event['action']):
            setattr(self, event['action'], self.send_notification)
        # self[event['action']] = self.send_notification
        self.send_json(event)
