from rest_framework.serializers import ModelSerializer, ValidationError

from AppraisalApp.models import Employee, Feedback, Competency


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['pk', 'username', 'employee_type', 'email', 'address', 'password']
        read_only_fields = ['pk']
        extra_kwargs = {'password': {'write_only': True}}


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

    def create(self, validated_data):
        from_user= validated_data.get('from_user')
        to_user= validated_data.get('to_user')
        if to_user.reports_to == from_user:
            return super().create(validated_data)
        else:
            raise ValidationError("Employee doesn't report to this user")


class CompetencySerializer(ModelSerializer):
    # feedback = FeedbackSerializer()

    class Meta:
        model = Competency
        fields = ['feedback', 'pk', 'comment', 'team_work', 'leadership']
        read_only_fields = ['pk']

    def validate_leadership(self, value):
        return self.check_value(value)

    def validate_team_work(self, value):
        return self.check_value(value)

    def check_value(self, value):
        value_checked = value if 1 >= value <= 10 else ValidationError("Value out of range")
        return value_checked
