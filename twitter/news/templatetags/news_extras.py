from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

ELLIPSIS = '...'
CENTER = 250
ACCURACY = 25
SEPARATOR_KEYS = ['.', ' ']


def get_closest_to_center(values, center):
    if values:
        return min(values, key=lambda x: abs(x - center))

def slice_string_to_key(string, key, accuracy, center):
    temp_indexs = (
        string.find(key, center, center + accuracy),
        string.rfind(key, center - accuracy, center),
    )

    indexs = [index for index in temp_indexs if not index == -1]
    index = get_closest_to_center(indexs, center)
    if index:
        return string[:index]


@register.filter()
@stringfilter
def excerpt_news(news_complete):
    if len(news_complete) <= CENTER:
        return news_complete

    for key in SEPARATOR_KEYS:
        news_excerpted = slice_string_to_key(news_complete, key, ACCURACY, CENTER)
        if news_excerpted:
            return news_excerpted + ELLIPSIS
    return news_complete[:CENTER] + ELLIPSIS


@register.inclusion_tag('news/news_card.html')
def show_news_card(news):
    return {'news': news}
