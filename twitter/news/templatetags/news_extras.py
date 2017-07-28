from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter('split_to_fullstop')
@stringfilter
def split_to_fullstop(value):
    return value.split('.')[0].split('!')[0]


@register.inclusion_tag('news/news_media_div.html')
def show_news_media_div(news):
    return {'news': news}
