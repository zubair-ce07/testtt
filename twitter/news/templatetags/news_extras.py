from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


def get_closest_to_center(values, center):
    if values:
        closest = values[0]
    else:
        return
    for value in values:
        if abs(center - value) < closest:
            closest = value
    return closest


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
    continue_ = '...'
    center = 250
    accuracy = 25
    keys = ['.', ' ']

    if len(news_complete) <= center:
        return news_complete

    for key in keys:
        news_excerpted = slice_string_to_key(news_complete, key, accuracy, center)
        if news_excerpted:
            return news_excerpted + continue_
    return news_complete[:center] + continue_


@register.inclusion_tag('news/news_card.html')
def show_news_card(news):
    return {'news': news}
