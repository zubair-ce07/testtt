from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def excerpt_news(news_complete):
    continue_ = '...'
    if len(news_complete) < 250:
        return news_complete
    if len(news_complete) > 250:
        news_excerpted = news_complete[:250] + news_complete[250:275].split('.')[0].split('!')[0]
        if not news_excerpted == news_complete:
            return news_excerpted + continue_
        else:
            news_excerpted = news_complete[:250] + news_complete[250:275].split(' ')[0]
            if not news_excerpted == news_complete:
                return news_excerpted + continue_
            else:
                return news_complete[:250] + continue_


@register.inclusion_tag('news/news_card.html')
def show_news_card(news):
    return {'news': news}
