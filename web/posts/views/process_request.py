from django.core.mail import EmailMessage
from django.views.generic import View
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

from web.posts.models import Request, Post


class ProcessRequestView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request, post_id, request_id, status):
        request_to_process = Request.objects.filter(pk=request_id)
        if request_to_process.exists() and \
                (status == Request.StatusChoices.ACCEPTED or status == Request.StatusChoices.REJECTED):
            request_to_process.update(status=status)
            self.send_email(status, request_to_process[0].requested_by)

            if status == Request.StatusChoices.ACCEPTED:
                post = Post.objects.get(pk=post_id)
                post.is_sold = True
                post.save()
                requests_to_be_rejected = post.requests.filter(status=Request.StatusChoices.PENDING)
                requests_to_be_rejected.update(status=Request.StatusChoices.REJECTED)
                for rejected_request in requests_to_be_rejected:
                    self.send_email(Request.StatusChoices.REJECTED, rejected_request.requested_by)

            response = redirect(reverse('my_post_details', args=[post_id]))
        else:
            response = render(request, 'web/404.html')

        return response

    # noinspection PyMethodMayBeStatic
    def send_email(self, status, user):

        if status == Request.StatusChoices.REJECTED:
            email = EmailMessage('eProperty - Offer Rejected',
                                 ' Your offer has been rejected. \n Regards, \n Team eProperty.',
                                 to=[user.email])
        else:
            email = EmailMessage('eProperty - Offer Accepted',
                                 ' Your offer has been Accepted. \n Regards, \n Team eProperty.',
                                 to=[user.email])
        email.send()