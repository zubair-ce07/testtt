from django import template

from ballot.models import Ballot

register = template.Library()


def addcss(field, css):
    return field.as_widget(attrs={"class": css})


register.filter('addcss', addcss)


@register.simple_tag
def recent_ballots(n=5):
    """Return recent n ballots"""
    ballots = Ballot.objects.get_active_ballots()
    return ballots[0:n]
