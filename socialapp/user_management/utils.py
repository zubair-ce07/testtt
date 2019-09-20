def get_request_notification_text(notification_type):
    return "You have a new {} request".format(notification_type)


FRIEND = 'friend'
GROUP = 'group'

NOTIFICATION_CHOICE_FIELDS = ((FRIEND, FRIEND), (GROUP, GROUP),)
