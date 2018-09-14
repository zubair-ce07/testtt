from .models import Question


def ballot_count(request):
    count = Question.objects.count()
    return {"question_count": count}
