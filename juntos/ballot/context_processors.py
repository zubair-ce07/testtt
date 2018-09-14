from .models import Question


def question_count(request):
    count = Question.objects.count()
    return {"question_count": count}
