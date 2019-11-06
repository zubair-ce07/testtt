from users.models import UserProfile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ['id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'location',
                  'age',
                  'phone_number',
                  'password'
        ]
        extra_kwargs = {"password":
                            {"write_only":True}
                            }
