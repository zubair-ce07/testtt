from django.core.mail import EmailMessage
from django.views.generic import View
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from web.posts.models import Request, Post


class AcceptRequestView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request, post_id, request_id):
        # TODO: not accepted yet, it would be request_to_process
        accepted_request = Request.objects.get(pk=request_id)
        accepted_request.status = 'accepted'
        accepted_request.save()
        self.send_email('accepted', accepted_request.requested_by)

        post = Post.objects.get(pk=post_id)
        post.is_sold = True
        post.save()

        for request in post.requests.all():
            if request != accepted_request:
                if request.status != 'rejected':
                    request.status = 'rejected'
                    request.save()
                    self.send_email('rejected', request.requested_by)

        return redirect(reverse('my_post_details', args=[post_id]))

    # noinspection PyMethodMayBeStatic
    def send_email(self, email_type, user):

        if email_type == 'rejected':
            email = EmailMessage('eProperty - Offer Rejected',
                                 ' Your offer has been rejected. \n Regards, \n Team eProperty.',
                                 to=[user.email])
        else:
            email = EmailMessage('eProperty - Offer Accepted',
                                 ' Your offer has been Accepted. \n Regards, \n Team eProperty.',
                                 to=[user.email])

        email.send()