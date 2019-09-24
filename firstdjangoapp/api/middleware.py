from django.contrib.auth.models import AnonymousUser, User
from django.utils.deprecation import MiddlewareMixin
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


def get_user_jwt(request):
    user = None
    try:
        user_jwt = JWTTokenUserAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            token_user = user_jwt[0]
            user_id = token_user.pk
            user = User.objects.get(id=user_id)
    except:
        pass
    return user or AnonymousUser()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = get_user_jwt(request)
        print(request.user)
