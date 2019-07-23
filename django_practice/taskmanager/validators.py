from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email_unique(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError(
            _('%(email)s already exists'),
            code='invalid',
            params={'email': email},
        )


def validate_username_unique(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError(
            _('%(username)s already exists'),
            code='invalid',
            params={'username': username},
        )
