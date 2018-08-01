from rest_framework import serializers
from teams.models import Team, Player, Photo, LiveScore


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'ranking', 'type', 'url', 'players', 'comments', 'follows']


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'DOB', 'playing_role', 'ranking', 'url', 'teams']

