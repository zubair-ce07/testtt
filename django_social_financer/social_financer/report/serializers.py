__author__ = 'abdul'
from rest_framework import serializers
from django.core import serializers as django_serializers

from .models import Report
from accounts.models import UserProfile


class ReportModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'

    def create(self, validated_data):
        new_Report = Report()
        new_Report.reported_user = self.instance
        user_id = self.context.get('by_user', -1)
        new_Report.reporting_user = UserProfile.objects.get(id=user_id)
        new_Report.category = validated_data['category']
        new_Report.comments = validated_data['comments']
        new_Report.save()
        return new_Report


class ViewReportsSerializer(serializers.Serializer):

    def to_representation(self, userprofile):
        return {
            'received_reports' : django_serializers.serialize('json', userprofile.received_reports.all()),
            'submitted_reports' : django_serializers.serialize('json', userprofile.submitted_report.all()),
        }
