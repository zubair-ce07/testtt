import re
from rest_framework import serializers
from web.constants import *


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(allow_blank=False, write_only=True)
    new_password = serializers.CharField(allow_blank=False, write_only=True)
    confirm_password = serializers.CharField(allow_blank=False, write_only=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        if self.user.check_password(data.get('old_password')):
            password = data.get('new_password')
            confirm_password = data.get('confirm_password')
            if password and confirm_password != password:
                raise serializers.ValidationError()
        else:
            raise serializers.ValidationError(ENTER_CORRECT_OLD_PASSWORD)
        return data

    # noinspection PyMethodMayBeStatic
    def validate_new_password(self, new_password):
        if len(new_password) < 8:
            raise serializers.ValidationError(PASSWORD_IS_TOO_SHORT)
        elif not re.search(r'[\W]+', new_password):
            raise serializers.ValidationError(MUST_HAVE_A_SPECIAL_CHARACTER)
        return new_password

    def create(self, validated_data):
        self.user.set_password(validated_data.get('new_password'))
        self.user.save()
        return self.user

    def update(self, instance, validated_data):
        return instance