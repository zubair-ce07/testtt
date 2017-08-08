from memoapp.models import User
from django.http import HttpResponseForbidden, HttpResponse, Http404

class CheckSuperUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        pass


    def __call__(self, request):
        if request.path == '/editprofile' and request.user.first_name == 'Ali':
            raise Http404
        else:
            return  self.get_response(request)
