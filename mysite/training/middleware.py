from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib import auth


class UserAuthentication(MiddlewareMixin):
    def get_user(self, request):
        if not hasattr(request, '_cached_user'):
            request._cached_user = auth.get_user(request)
        return request._cached_user

    def process_request(self, request):
        if hasattr(request, 'session'):
            request.user = SimpleLazyObject(lambda: self.get_user(request))
        else:
            raise Exception("Session Middleware not Installed")
