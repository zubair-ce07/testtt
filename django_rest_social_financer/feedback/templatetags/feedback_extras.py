__author__ = 'abdul'

from django import template

register = template.Library()

@register.filter(name='get_reverse')
def get_reverse_url(role):
    return 'accounts:my_consumers' if role == 'DN' else 'accounts:home'
