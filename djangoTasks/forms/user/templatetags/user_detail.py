from django import template


register = template.Library()


@register.filter(is_safe=True)
def details(user):
    return "{} \n {}".format(user.get_full_name(), user.email)
