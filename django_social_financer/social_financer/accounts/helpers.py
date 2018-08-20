
def feedback_or_report(request):
    reverse_url = ''
    if str(request.POST.get('feedback_request', '')):
        reverse_url = 'accounts:give_feedback'

    elif str(request.POST.get('report_request', '')):
        reverse_url = 'accounts:report_user'
    consumer_id = int(request.POST.get('consumer_id', '-1'))
    return (reverse_url, consumer_id)

