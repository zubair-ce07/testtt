from django.core.exceptions import ValidationError
from drf_braces.serializers.form_serializer import FormSerializer

from . import forms


class UserFormSerializer(FormSerializer):
    class Meta:
        form = forms.UserCreationForm
        fields = ['__all__']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise ValidationError("passwords don't match")
        return data

