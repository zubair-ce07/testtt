from rest_framework import serializers


class HomepageSerializer(serializers.Serializer):
    bio = serializers.TextField(required=False, max_length=500)
    location = serializers.CharField(required=False, max_value=30)
    birth_date = serializers.DateField(required=False, allow_null=True)
