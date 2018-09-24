"""
this module contains the custom middlewares for this django app
"""
from django.contrib import auth
from django.utils.functional import SimpleLazyObject


class MyAuthMiddleware:
    """
    this is the custom authentication middleware class which checks whether a user is
     authenticated or not
    """

    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_request(self, request):
        """
        this method is required for middleware as it process every request
        :param request:
        :return:
        """
        assert hasattr(request, 'session')
        request.user = SimpleLazyObject(lambda: get_user(request))


def get_user(request):
    """
    this function checks that a user is present in our DB, if yes, return it
    :param request:
    :return:
    """
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user
