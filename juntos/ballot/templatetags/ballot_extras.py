from django import template

from ballot.models import Question

register = template.Library()


@register.filter(name='uppers')
def upper1(value):
    """Converts a string into all uppercase"""
    return value.upper()[0:2]



def addcss(field, css):
    return field.as_widget(attrs={"class": css})


register.filter('addcss', addcss)


@register.simple_tag
def recent_ballots(n=5, **kwargs):
    """Return recent n ballots"""
    name = kwargs.get("name")
    questions = Question.objects.all().order_by('-created_at')
    if name:
        questions = questions.filter(name=name)
    return questions[0:n]
