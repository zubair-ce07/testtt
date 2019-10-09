from rest_framework import serializers
from .models import Program, Campus


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['name']


class ProgramSerializer(serializers.ModelSerializer):
    campus = CampusSerializer(read_only=True)

    class Meta:
        model = Program
        fields = ['name', 'category', 'campus']
