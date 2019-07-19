from rest_framework import serializers

from cv_maker_app.models import Job


class JobSerializer(serializers.HyperlinkedModelSerializer):
    skill1 = serializers.CharField(allow_blank=True)
    skill2 = serializers.CharField(allow_blank=True)
    skill3 = serializers.CharField(allow_blank=True)
    class Meta:
        model = Job
        fields = ['title', 'city', 'experience', 'description', 'skill1', 'skill2', 'skill3']
