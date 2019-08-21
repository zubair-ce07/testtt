from django.core.exceptions import ValidationError
from drf_braces.serializers.form_serializer import FormSerializer

from .forms import UserCreationForm
from .models import User


class UserFormSerializer(FormSerializer):
    class Meta:
        form = UserCreationForm
        fields = ['__all__']

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password_']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        date_of_birth = validated_data['date_of_birth']
        gender = validated_data['gender']
        kwargs = {
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'gender': gender
        }
        User.objects.create_user(**kwargs)

    def validate(self, data):
        super().validate(data)
        if data['password_'] != data['confirm_password']:
            raise ValidationError("passwords don't match")
        return data

