__author__ = 'abdul'
from datetime import datetime

from rest_framework import serializers
from django.core import serializers as django_serializers

from accounts.models import UserProfile
from report.models import Report


class ReportModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Report
        exclude = ('reporting_user', 'reported_user')

    def update(self, instance, validated_data):
        print('here1')
        new_Report = Report()
        new_Report.reported_user = instance
        user_id = self.context.get('by_user', -1)
        new_Report.reporting_user = UserProfile.objects.get(id=user_id)
        new_Report.category = validated_data['category']
        new_Report.comments = validated_data['comments']
        new_Report.date_logged = datetime.now()
        new_Report.save()
        return new_Report

class ViewReportsSerializer(serializers.Serializer):

    def to_representation(self, userprofile):
        return {
            'received_reports' : django_serializers.serialize('json', userprofile.received_reports.all()),
            'submitted_reports' : django_serializers.serialize('json', userprofile.submitted_report.all()),
        }
