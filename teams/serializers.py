from rest_framework import serializers
from teams.models import Team, Player, Photo, LiveScore


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        exclude = ['is_active', 'DOB', 'batting_style', 'bowling_style']
