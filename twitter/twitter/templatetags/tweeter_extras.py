from django import template

register = template.Library()


@register.simple_tag(name='users_name')
def firstname_or_username(user):
    if user.first_name:
        return user.first_name
    return user.username
