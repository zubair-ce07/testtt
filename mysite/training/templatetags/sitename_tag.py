from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def sitename_tag():
    return getattr(settings, "SITE_NAME", "MySite")
