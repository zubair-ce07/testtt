import re
from django.conf import settings
from django.shortcuts import redirect

EXEMPT_URLS = [re.compile(settings.LOGIN_URL)]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += (re.compile(url) for url in settings.LOGIN_EXEMPT_URLS)


class LoginRequiredMiddleware:

    def __init__(self, get_request):
        self.get_request = get_request

    def __call__(self, request,  *args, **kwargs):
        response = self.get_request(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        print(f'Request In Middleware: {path}')

        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        if request.user.is_authenticated and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated or url_is_exempt:
            return None
        else:
            return redirect(settings.LOGIN_URL)
