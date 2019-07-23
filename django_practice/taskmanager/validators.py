from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def validate_user_profile_picture(avatar):
    width, height = get_image_dimensions(avatar)

    # validate dimensions
    max_width = max_height = 500
    if width > max_width or height > max_height:
        raise ValidationError(
            u'Please use an image that is '
            '%s x %s pixels or smaller.' % (max_width, max_height))

    # validate content type
    file_type, extension = avatar.content_type.split('/')
    if not (file_type == 'image' and extension in ['jpeg', 'gif', 'png']):
        raise ValidationError(u'Please use a JPEG, '
                              'GIF or PNG image.')

    # validate file size
    if len(avatar) > (20 * 1024):
        raise ValidationError(
            u'Avatar file size may not exceed 20k.')
