from rest_framework.serializers import ModelSerializer
from AppraisalApp.models import Employee, Feedback, Competency


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['pk', 'username', 'employee_type', 'email', 'address', 'password']
        read_only_fields = ['pk']
        extra_kwargs = {'password': {'write_only': True}}


class CompetencySerializer(ModelSerializer):
    class Meta:
        model = Competency
        fields = ['pk', 'comment', 'team_work', 'leadership']
        read_only_fields = ['pk']


class CompetencyFeedbackSerializer(ModelSerializer):
    competency_set = CompetencySerializer(many=True)

    def create(self, validated_data):
        from_user = validated_data.get('from_user')
        to_user = validated_data.get('to_user')

        feedback = Feedback(from_user=from_user, to_user=to_user)
        feedback.save()

        competency_sets = validated_data.get('competency_set')
        for competency_set in competency_sets:
            competency = Competency(**competency_set, feedback=feedback)
            competency.save()

        return feedback

    def update(self, instance, validated_data):
        instance.to_user = validated_data.get('to_user', instance.to_user)
        instance.save()
        instance_competency = instance.competency_set.all()
        competency_sets = validated_data.get('competency_set')
        if instance_competency:
            competency = instance_competency.first()
            for competency_set in competency_sets:
                competency.comment = competency_set.get('comment', competency.comment)
                competency.leadership = competency_set.get('leadership', competency.leadership)
                competency.team_work = competency_set.get('team_work', competency.team_work)
                competency.save()
        else:
            for competency_set in competency_sets:
                competency = Competency(**competency_set, feedback=instance)
                competency.save()

        return instance

    class Meta:
        model = Feedback
        fields = ['competency_set', 'from_user', 'to_user']
