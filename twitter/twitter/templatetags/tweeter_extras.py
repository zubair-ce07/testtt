from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
def split_to_fullstop(value):
    return value.split('.')[0].split('!')[0]

register.filter('split_to_fullstop', split_to_fullstop)