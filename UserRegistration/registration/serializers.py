from django.core.exceptions import ValidationError
from drf_braces.serializers.form_serializer import FormSerializer

from .forms import UserCreationForm
from .models import User


class UserFormSerializer(FormSerializer):
    class Meta:
        form = UserCreationForm
        fields = ['__all__']

    def create(self, validated_data):
        User.objects.create_user(
            validated_data['email'],
            validated_data['password_'],
            validated_data['first_name'],
            validated_data['last_name'],
            validated_data['date_of_birth'],
            validated_data['gender']
        )

    def validate(self, data):
        super().validate(data)
        if data['password_'] != data['confirm_password']:
            raise ValidationError("passwords don't match")
        return data

