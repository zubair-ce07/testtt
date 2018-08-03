from django import template
from datetime import date

register = template.Library()


@register.filter
def truncate_string(original_string, limit):
    """ Truncates the string to a given limit and adds continuation string """
    if len(original_string) <= limit:
        return original_string
    else:
        return original_string[:limit] + " ..."


@register.filter
def due_date_string(my_date):
    """ Convert the given due date to a human readable format """
    delta = my_date - date.today()

    if delta.days == 0:
        return "Today!"
    elif delta.days < 0:
        return "%s %s ago!" % (abs(delta.days),
                               ["days", "day"][abs(delta.days) == 1])
    elif delta.days == 1:
        return "Tomorrow"
    elif delta.days > 0:
        return "In %s days" % delta.days


