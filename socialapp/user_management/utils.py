def get_notification_text(notification_type):
    return "You Have a new {} request".format(notification_type)


NOTIFICATION_CHOICE_FIELDS = (('friend', 'Friend'), ('group', 'Group'),)
