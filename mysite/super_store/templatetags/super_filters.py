from django import template

register = template.Library()


@register.filter(name='sub')
def sub(value, arg):
    return value - arg


@register.filter(name='id_name')
def id_name(value, arg):
    return str(value) + '-' + arg
