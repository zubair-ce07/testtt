from rest_framework import serializers
from movies.serializers import RoleSerializer, MetaMovieSerializer
from users.serializers import UserSerializer
from watchlists.models import WatchListItem, Activity


class ActivitySerializer(serializers.ModelSerializer):
    def get_rating(self, watchlist_item):
        return watchlist_item.get_rating_display()

    def get_actions(self, watchlist_item):
        added_at, watched_at, recommended_at, rated_at, voted_actor_at = (0, 0, 0, 0, 0)
        for activity in watchlist_item.activity_set.all():
            if activity.type == Activity.ADDED:
                added_at = activity.created_at
            elif activity.type == Activity.WATCHED:
                watched_at = activity.created_at
            elif activity.type == Activity.RECOMMENDED:
                recommended_at = activity.created_at
            elif activity.type == Activity.RATED:
                rated_at = activity.created_at
            elif activity.type == Activity.VOTED_ACTOR:
                voted_actor_at = activity.created_at
        return {
            'added_at': added_at, 'watched_at': watched_at, 'recommended_at': recommended_at,
            'rated_at': rated_at, 'voted_actor_at': voted_actor_at
        }

    actions = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    best_actor = RoleSerializer()
    movie = MetaMovieSerializer()
    user = UserSerializer()

    class Meta:
        model = WatchListItem
        fields = ['id', 'actions', 'best_actor', 'rating',  'user', 'movie']
