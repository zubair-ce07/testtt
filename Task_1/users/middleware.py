from django.contrib import auth
from django.utils.functional import SimpleLazyObject

from users.models import UserProfile


class AuthenticationMiddleware(object):
    def get_user(self, request):
        if not hasattr(request, '_cached_user'):
            request._cached_user = auth.get_user(request)
        return request._cached_user

    def get_user_profile(self, request):
        if not hasattr(request, '_cached_user_profile'):
            request._cached_user_profile = UserProfile.objects.get(user=request.user)
        return request._cached_user_profile

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert hasattr(request, 'session'), 'Session middleware is not installed in settings'
        request.user = SimpleLazyObject(lambda: self.get_user(request))
        request.userprofile = SimpleLazyObject(lambda: self.get_user_profile(request))
        return self.get_response(request)
