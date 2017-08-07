from rest_framework import serializers

from users.models import UserProfile


class EditSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, source='user.first_name', required=False, allow_blank=True,
                                       style={'placeholder': 'e.g. John (Optional)'})
    last_name = serializers.CharField(max_length=30, source='user.last_name', required=False, allow_blank=True,
                                      style={'placeholder': 'e.g. Doe (Optional)'})
    email = serializers.EmailField(source='user.email', style={'placeholder': 'Email Address'})

    def update(self, instance, validated_data):
        if not validated_data.get('image'):
            validated_data.pop('image')
        user = self.instance.user
        user_data = validated_data.pop('user')
        user.email = user_data.pop('email')
        user.first_name = user_data.pop('first_name')
        user.last_name = user_data.pop('last_name')
        user.save()
        return super(EditSerializer, self).update(instance, validated_data)

    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'address', 'image', 'country',)
