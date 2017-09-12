from rest_framework import serializers
from movies.serializers import RoleSerializer, MovieSerializer
from users.serializers import UserSerializer
from watchlists.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    def get_activity_type(self, activity):
        return activity.get_type_display()

    def get_role(self, activity):
        if activity.type == Activity.VOTED_ACTOR:
            return RoleSerializer(activity.watchlist.best_actor).data

    activity_type = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    movie = MovieSerializer(source='watchlist.movie', context={'description': 'short'})
    user = UserSerializer(source='watchlist.user')

    class Meta:
        model = Activity
        fields = ['role', 'created_at', 'activity_type', 'movie', 'user']
