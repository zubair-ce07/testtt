from django.contrib import auth
from django.utils.functional import SimpleLazyObject

from users.models import UserProfile


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user


def get_user_profile(request):
    if not hasattr(request, '_cached_user_profile'):
        request._cached_user_profile = UserProfile.objects.get(user__username=request.user.username)
    return request._cached_user_profile


class AuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert hasattr(request, 'session'), 'Session middleware is not installed in settings'
        request.user = SimpleLazyObject(lambda: get_user(request))
        request.userprofile = SimpleLazyObject(lambda: get_user_profile(request))
        response = self.get_response(request)
        return response
