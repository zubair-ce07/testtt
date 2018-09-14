from django.db.models import Avg

from feedback.models import Feedback
from accounts.models import UserProfile

def feedback_or_report(request):
    reverse_url = ''
    if str(request.POST.get('feedback_request', '')):
        reverse_url = 'accounts:give_feedback'

    elif str(request.POST.get('report_request', '')):
        reverse_url = 'accounts:report_user'
    consumer_id = int(request.POST.get('consumer_id', '-1'))
    return (reverse_url, consumer_id)

def get_user_rating(userprofile):
    rating = Feedback.objects.filter(given_to_user=userprofile).aggregate(Avg('star_rating'))
    return rating.get('star_rating__avg','Not rated yet')
