from django.contrib.auth import get_user_model
from rest_framework import serializers
from system.models import Appraisal, Competence
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'password', 'title', 'department'
        ]

    def validate(self, object):
        object['password'] = make_password(object['password'])
        return object

    def create(self, validated_data):
        return User.objects.create(user_level="employee", **validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk', 'username', 'first_name', 'last_name',
            'email', 'password', 'title', 'department',
            'user_level', 'report_to'
        ]
    read_only_fields = ['pk']

    def validate(self, object):
        user = None
        request = self.context.get("request")
        user = request.user
        if user.user_level == "admin":
            object['password'] = make_password(object['password'])
            return object
        else:
            raise serializers.ValidationError(
                {'Permission-Denied': 'You do not have '
                               'permission for this operation'})


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ('decision_making','confidence','problem_solving')


class AppraisalSerializer(serializers.ModelSerializer):
    competence_set = CompetenceSerializer(many=True)
    class Meta:
        model = Appraisal
        fields = ('pk', 'description', 'comment', 'to_user', 'competence_set')
        read_only_fields = ['pk']

    def validate(self, object):
        user = self.context.get("request").user
        to_user = object.get("to_user")
        if to_user.report_to == user:
            if user.user_level == "employee":
                raise serializers.ValidationError(
                    {'Permission-Denied': 'You do not have '
                                   'permission for this operation'})
            return object
        else:
            raise serializers.ValidationError(
                {'Permission-Denied': 'You are not allowed to give '
                               'appraisal to this employee'})

    def create(self, validated_data):
        user = self.context.get("request").user
        competencies_data = validated_data.pop("competence_set")
        app = Appraisal.objects.create(from_user=user, **validated_data)
        for competencies in competencies_data:
            app.competence_set.create(**competencies)
        return app

    def update(self, instance, validated_data):
        competencies_data = validated_data.pop('competence_set')
        competencies = (instance.competence_set).all()
        competencies = list(competencies)

        instance.to_user = validated_data.get(
            'to_user', instance.to_user)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.comment = validated_data.get(
            'comment', instance.comment)
        instance.save()

        for new_competencies in competencies_data:
            old_competencies = competencies.pop(0)
            old_competencies.confidence = new_competencies.get(
                'confidence', old_competencies.confidence)
            old_competencies.decision_making = new_competencies.get(
                'decision_making', old_competencies.decision_making)
            old_competencies.problem_solving = new_competencies.get(
                'problem_solving', old_competencies.problem_solving)
            old_competencies.save()
        return instance

