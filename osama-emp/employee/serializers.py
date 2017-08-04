from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the employee class
    """
    profile = serializers.HyperlinkedIdentityField(
        view_name='employee-detail', read_only=True, lookup_field='username'
    )
    directs = serializers.HyperlinkedIdentityField(
        view_name='directs', format='json', lookup_field='username')
    reports_to = serializers.HyperlinkedRelatedField(
        view_name='employee-detail', read_only=True, lookup_field='username'
    )

    class Meta:
        model = Employee
        fields = ('username', 'profile', 'first_name', 'last_name', 'gender',
                  'date_of_birth', 'date_of_joining', 'job_title',
                  'nationality', 'reports_to', 'directs',)
        extra_kwargs = {
            'url': {'view_name': 'employee-detail', 'lookup_field': 'username'},
        }

    def create(self, validated_data, *args, **kwargs):
        """
        Create method override that ensures that a django User model is created
        alongside with each employee
        """
        user_data = {
            'username': validated_data['username'],
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
        }
        user = User.objects.create(**user_data)
        return Employee.objects.create(user=user, **validated_data)
