__author__ = 'abdul'
from django import template

register = template.Library()

@register.filter(name='formatted_address')
def get_formatted_address(url, address):
    return '{}{}'.format(url, '+'.join(address.split(' ')))

@register.filter(name='categories')
def get_categories(categories):
    return ', '.join([category.name for category in categories.all()])

@register.filter(name='consumer_heading')
def get_heading(donor):
    negative_heading = "No Donor has selected you yet."
    positive_heading = "Following are the details of your Donor"
    return negative_heading if donor is None else positive_heading