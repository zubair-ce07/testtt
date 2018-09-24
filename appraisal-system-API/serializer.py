from django.contrib.auth import get_user_model
from rest_framework import serializers
from system.models import Appraisal, Competence
from django.contrib.auth.hashers import make_password


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'password', 'title', 'department',
            'user_level', 'report_to'
        ]

    def validate(self, object):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.user_level=="admin":
                object['password'] = make_password(object['password'])
                return object
            else:
                raise serializers.ValidationError(
                    "You do not have permission for this operation")
        else:
            raise serializers.ValidationError("You are not logged in")


class AppraisalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appraisal
        fields = ('pk','description', 'comment', 'to_user')
        read_only_fields=['pk']


class CompetenceSerializer(serializers.ModelSerializer):
    appraisal = AppraisalSerializer()

    class Meta:
        model = Competence
        fields = ('appraisal', 'decision_making', 'confidence', 'problem_solving')

    def create(self, validated_data):
        user = self.context.get("request").user
        appraisal_data = self.validated_data.get('appraisal')
        app = Appraisal.objects.create(from_user=user,**appraisal_data)
        return Competence.objects.create(
            appraisal=app,
            decision_making=validated_data['decision_making'],
            confidence=validated_data['confidence'],
            problem_solving=validated_data['problem_solving']
        )

    def update(self, instance, validated_data):
        appraisal_data = validated_data.pop('appraisal')
        instance.decision_making = validated_data.get(
            'decision_making', instance.decision_making)
        instance.confidence = validated_data.get(
            'confidence', instance.confidence)
        instance.problem_solving = validated_data.get(
            'problem_solving', instance.problem_solving)
        instance.appraisal.to_user = appraisal_data.get(
            'to_user', instance.appraisal.to_user)
        instance.appraisal.description = appraisal_data.get(
            'description', instance.appraisal.description)
        instance.appraisal.comment = appraisal_data.get(
            'comment', instance.appraisal.comment)
        instance.save()
        return instance

    def validate(self, object):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.user_level == "employee":
                raise serializers.ValidationError(
                    "You do not have permission for this operation")
            return object
        else:
            raise serializers.ValidationError("You are not logged in")
