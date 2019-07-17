from rest_framework import serializers
from cv_maker_app.models import Job


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'city', 'experience', 'description', 'skill1', 'skill2', 'skill3']
