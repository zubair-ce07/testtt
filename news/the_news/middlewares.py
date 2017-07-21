__author__ = 'luqman'


from django.conf import settings
from django.http import HttpResponseForbidden


class IpFilterMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR', None)
        if ip and ip in settings.ALLOWED_IP_LIST:
            response = self.get_response(request)
        else:
            response = HttpResponseForbidden()

        return response
