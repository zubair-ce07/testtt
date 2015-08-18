from django.core.mail import EmailMessage
from django.views.generic import View
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from web.posts.models import Request


#TODO: merge this in the process request URL.
class RejectRequestView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request, post_id, request_id):
        rejected_request = Request.objects.get(pk=request_id)
        rejected_request.status = 'rejected'
        rejected_request.save()
        self.send_rejection_email(rejected_request.requested_by)
        return redirect(reverse('my_post_details', args=[post_id]))

    # noinspection PyMethodMayBeStatic
    def send_rejection_email(self, user):
        email = EmailMessage('eProperty - Offer Rejected',
                             ' Your offer has been rejected. \n Regards, \n Team eProperty.',
                             to=[user.email])
        email.send()