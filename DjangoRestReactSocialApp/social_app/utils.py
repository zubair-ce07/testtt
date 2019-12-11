from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def notify_on_socket(action, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'social_app',
        {
            'type': 'send.notification',
            'action': action,
            'payload': {
                "data": data
            }
        }
    )
