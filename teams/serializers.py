from collections import defaultdict

from django.db.models import Q
from rest_framework import serializers
from teams.models import Team, Player, Photo, LiveScore, BattingAverage, BowlingAverage


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    formats = serializers.StringRelatedField(many=True)
    teams = serializers.StringRelatedField(many=True)

    class Meta:
        model = Player
        exclude = ['is_active', 'DOB', 'batting_style', 'bowling_style']


class BattingAverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattingAverage
        fields = ['id', 'player', 'format', 'highest_score']


class PlayerFormatSearchSerializer(serializers.Serializer):
    players = serializers.SerializerMethodField()

    def get_players(self, obj):
        query_dict = self.context['search']
        queryset1 = Player.objects.all().order_by('id')
        if query_dict:
            print(query_dict)
            if 'formats' in query_dict:
                queryset1 = queryset1 & queryset1.filter(Q(batting_averages__format__iexact=query_dict.get('formats')))
            if 'role' in query_dict:
                queryset1 = queryset1 & queryset1.filter(Q(playing_role__iexact=query_dict.get('role')))
            if 'ranking' in query_dict:
                queryset1 = queryset1 & queryset1.filter(Q(ranking__gte=query_dict.get('ranking')))

        return PlayerSerializer(instance=queryset1, many=True).data