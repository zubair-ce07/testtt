from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from watchlists.models import WatchListItem, Activity
from watchlists.serializers import ActivitySerializer
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
    Activity.objects.get_or_create(watchlist=watchlist_item, type=activity_type)


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
        response = 'Added'
        create_activity(watchlist_item, Activity.ADDED)
    else:
        response = 'Removed'
        delete_activity(watchlist_item, Activity.ADDED)

    return Response({'status': response})


# URL: <host>/movies/<movie_id>/<action_type[watched or recommended]>/
@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def changed_watchlist_status(request, movie_id, action_type):
    movie = get_movie(movie_id)
    watchlist_item = get_watchlist_item(request.user, movie)

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

    return Response({'status': 'Saved'})


# URL: <host>/movies/<movie_id>/ratings/<action[liked or disliked]>/
@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated])
def rate_movie(request, movie_id, action):
    movie = get_movie(movie_id)
    watchlist_item = get_watchlist_item(request.user, movie)
    watchlist_item.rating = WatchListItem.LIKED if action == 'liked' else WatchListItem.DISLIKED
    create_activity(watchlist_item, Activity.RATED)
    watchlist_item.save()
    return Response({'status': 'Saved'})


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
    return Response({'status': 'Saved'})


# URL: <host>/activities/
@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def get_activities(request):
    following_users = request.user.follows.all()
    activities = Activity.objects.filter(watchlist__user__in=following_users)
    return Response(ActivitySerializer(activities, many=True).data)
