from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import logging


logger = logging.getLogger(__name__)


class AuthBackend(object):

    def authenticate(self, username=None, email=None, password=None):

        if email:
            user_value = email
            logger.debug("Logging in using email")
        elif username:
            user_value = username
            logger.debug("Logging in using email")

        try:
            user = User.objects.get(email=user_value)
            if user.check_password(password):
                logger.info("Successful login")
                return user

        except ObjectDoesNotExist, e:
            logger.exception(e)
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except ObjectDoesNotExist, e:
            logger.exception(e)
            return None
