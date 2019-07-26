from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def validate_email_unique(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError(
            '%(email)s already exists',
            code='invalid',
            params={'email': email},
        )


def validate_username_unique(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError(
            '%(username)s already exists',
            code='invalid',
            params={'username': username},
        )


def validate_user_profile_picture(avatar):
    w, h = get_image_dimensions(avatar)

    # validate dimensions
    max_width = max_height = 500
    if w > max_width or h > max_height:
        raise ValidationError(
            u'Please use an image that is '
            '%s x %s pixels or smaller.' % (max_width, max_height))

    # validate content type
    main, sub = avatar.content_type.split('/')
    if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
        raise ValidationError(u'Please use a JPEG, '
                              'GIF or PNG image.')

    # validate file size
    if len(avatar) > (20 * 1024):
        raise ValidationError(
            u'Avatar file size may not exceed 20k.')
