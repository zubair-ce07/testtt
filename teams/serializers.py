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


class BowlingAverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BowlingAverage
        fields = ['id', 'player', 'format', 'wickets']


class PlayerInsightsSearchSerializer(serializers.Serializer):
    players = serializers.SerializerMethodField()

    def get_players(self, obj):
        exact_queries = ['formats', 'playing_role', 'batting_style', 'bowling_style']
        query_dict = self.context['search']
        queryset = Player.objects.all().order_by('id')
        player_fields = [f.name for f in Player._meta.get_fields()]
        for key in query_dict:
            if key in exact_queries:
                query_string = {'{0}__{1}'.format(key, 'iexact'): query_dict[key]}
                if key == 'formats':
                    query_string = {'{0}__{1}'.format('batting_averages__format', 'iexact'): query_dict[key]}
                queryset = queryset.filter(**query_string).order_by('id')
            else:
                min_limit, max_limit = query_dict[key].split('_')
                category = key.split('.')
                if min_limit == '':
                    if key in player_fields:
                        query_string = {'{0}__{1}'.format(key, 'lte'): max_limit}
                    else:
                        query_string = {'{0}_{1}__{2}__{3}'.format(category[0], 'averages', category[1], 'lte'): max_limit}
                    queryset = queryset.filter(**query_string).order_by('id')
                elif max_limit == '':
                    if key in player_fields:
                        query_string = {'{0}__{1}'.format(key, 'gte'): min_limit}
                    else:
                        query_string = {'{0}_{1}__{2}__{3}'.format(category[0], 'averages', category[1], 'gte'): min_limit}
                    queryset = queryset.filter(**query_string).order_by('id')
                elif max_limit and min_limit:
                    if key in player_fields:
                        greater_query = {'{0}__{1}'.format(key, 'gte'): min_limit}
                        lesser_query = {'{0}__{1}'.format(key, 'lte'): max_limit}
                    else:
                        greater_query = {'{0}_{1}__{2}__{3}'.format(category[0], 'averages', category[1], 'gte'): min_limit}
                        lesser_query = {'{0}_{1}__{2}__{3}'.format(category[0], 'averages', category[1], 'lte'): max_limit}
                    queryset = queryset.filter(**greater_query, **lesser_query).order_by('id')

        return PlayerSerializer(instance=queryset, many=True).data