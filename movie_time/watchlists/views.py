from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from watchlists.models import WatchListItem, Activity
from watchlists.serializers import ActivitySerializer
from movies.serializers import WatchListItemSerializer, MovieSerializer
from movies.models import Movie, Role


def get_movie(movie_id):
    try:
        return Movie.objects.get(id=movie_id)
    except ObjectDoesNotExist:
        raise NotFound()


def get_watchlist_item(user, movie):
    try:
        return WatchListItem.objects.get(movie=movie, user=user)
    except ObjectDoesNotExist:
        raise NotFound()


def create_activity(watchlist_item, activity_type):
    activity, created = Activity.objects.get_or_create(watchlist=watchlist_item, type=activity_type)
    if not created:
        activity.created_at = timezone.now()
        activity.save()


def delete_activity(watchlist_item, activity_type):
    try:
        Activity.objects.get(watchlist=watchlist_item, type=activity_type).delete()
    except ObjectDoesNotExist:
        pass


# URL: <host>/movies/<movie_id>/watchlist/
@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def add_or_remove_from_watchlist(request, movie_id):
    movie = get_movie(movie_id)

    try:
        watchlist_item = get_watchlist_item(request.user, movie)
        watchlist_item.removed = False if request.method == 'PUT' else True
        watchlist_item.save()
    except NotFound:
        if request.method == 'PUT':
            watchlist_item = WatchListItem.objects.create(movie=movie, user=request.user)
        else:
            raise

    if request.method == 'PUT':
        create_activity(watchlist_item, Activity.ADDED)
    else:
        delete_activity(watchlist_item, Activity.ADDED)

    return Response(WatchListItemSerializer(watchlist_item).data)


# URL: <host>/movies/<movie_id>/<action_type[watched or recommended]>/
@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def changed_watchlist_status(request, movie_id, action_type):
    movie = get_movie(movie_id)
    watchlist_item = get_watchlist_item(request.user, movie)

    if action_type not in ['watched', 'recommended']:
        raise NotFound()

    if action_type == 'watched':

        if request.method == 'PUT':
            watchlist_item.is_watched = True
            create_activity(watchlist_item, Activity.WATCHED)
        else:
            watchlist_item.is_watched = False
            delete_activity(watchlist_item, Activity.WATCHED)

    elif action_type == 'recommended':

        if request.method == 'PUT':
            watchlist_item.is_recommended = True
            create_activity(watchlist_item, Activity.RECOMMENDED)
        else:
            watchlist_item.is_recommended = False
            delete_activity(watchlist_item, Activity.RECOMMENDED)

    watchlist_item.save()

    return Response(WatchListItemSerializer(watchlist_item).data)


# URL: <host>/movies/<movie_id>/ratings/<action[liked or disliked]>/
@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def rate_movie(request, movie_id, action):
    movie = get_movie(movie_id)
    watchlist_item = get_watchlist_item(request.user, movie)

    if request.method == 'PUT':
        watchlist_item.rating = WatchListItem.LIKED if action == 'Liked' else WatchListItem.DISLIKED
        create_activity(watchlist_item, Activity.RATED)
    else:
        watchlist_item.rating = None
        delete_activity(watchlist_item, Activity.RATED)

    watchlist_item.save()
    return Response(WatchListItemSerializer(watchlist_item).data)


# URL: <host>/roles/<role_id>/vote-up/
@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated])
def change_best_actor_vote(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
    except ObjectDoesNotExist:
        raise NotFound()

    watchlist_item = get_watchlist_item(request.user, role.movie)
    watchlist_item.best_actor = role
    create_activity(watchlist_item, Activity.VOTED_ACTOR)
    watchlist_item.save()
    return Response(WatchListItemSerializer(watchlist_item).data)


class GetActivities(ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        following_users = self.request.user.follows.all()
        return WatchListItem.objects.filter(user__in=following_users, removed=False).order_by(
            '-updated_at').select_related('movie__release_date', 'user', 'user__auth_token').prefetch_related(
            'activity_set', 'movie__genres', 'movie__images', 'movie__watchlist_items__user')


class GetUserActivities(ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user.follows.all().filter(id=self.kwargs['user_id'])
        return WatchListItem.objects.filter(user=user, removed=False).order_by(
            '-updated_at').select_related('movie__release_date', 'user', 'user__auth_token').prefetch_related(
            'activity_set', 'movie__genres', 'movie__images', 'movie__watchlist_items__user')


class GetToWatchList(ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Movie.objects.filter(watchlist_items__user=self.request.user, watchlist_items__is_watched=False,
                                    status='Released', watchlist_items__removed=False).select_related(
            'release_date').prefetch_related('watchlist_items__user', 'images', 'genres').order_by('title')


class GetWatchedList(ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Movie.objects.filter(watchlist_items__user=self.request.user, watchlist_items__removed=False,
                                    watchlist_items__is_watched=True).select_related(
            'release_date').prefetch_related('watchlist_items__user', 'images', 'genres').order_by('title')


class GetUpcomingList(ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Movie.objects.filter(watchlist_items__user=self.request.user, watchlist_items__is_watched=False,
                                    watchlist_items__removed=False).exclude(status='Released').select_related(
            'release_date').prefetch_related('watchlist_items__user', 'images', 'genres').order_by('title')
