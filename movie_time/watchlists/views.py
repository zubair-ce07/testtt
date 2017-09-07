from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from watchlists.models import WatchListItem
from movies.models import Movie, Role


def get_movie(data):
    movie_id = data.get('movie_id')
    if not movie_id:
        raise ParseError()

    try:
        return Movie.objects.get(movie_id)
    except ObjectDoesNotExist:
        raise NotFound()


def get_watchlist_item(user, movie):
    try:
        return WatchListItem.objects.get(movie=movie, user=user)
    except ObjectDoesNotExist:
        raise NotFound()


def update_watchlist(data, user, update_type):
    movie = get_movie(data)

    status = data.get('status')
    if not status:
        raise ParseError()

    watchlist_item = get_watchlist_item(user, movie)

    if update_type == 'watched':
        watchlist_item.is_watched = True if status == 'add' else False
    elif update_type == 'recommended':
        watchlist_item.is_recommended = True if status == 'add' else False
    elif update_type == 'rating':
        watchlist_item.rating = WatchListItem.LIKED if status == 'liked' else WatchListItem.DISLIKED
    watchlist_item.save()


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def add_or_remove_from_watchlist(request):
    movie = get_movie(request.data)

    status = request.data.get('status')
    if not status:
        raise ParseError()

    try:
        watchlist_item = get_watchlist_item(request.user, movie)
        watchlist_item.removed = False if status == 'add' else True
        watchlist_item.save()
    except NotFound:
        if status == 'add':
            WatchListItem.objects.create(movie=movie, user=request.user)
        else:
            raise

    response = 'Added' if status == 'add' else 'Removed'
    return Response({'status': response})


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def changed_watchlist_status(request, status_type):
    if status_type == 'watched':
        update_watchlist(request.data, request.user, 'watched')
    elif status_type == 'recommended':
        update_watchlist(request.data, request.user, 'recommended')
    elif status_type == 'rating':
        update_watchlist(request.data, request.user, 'rating')
    return Response({'status': 'Saved'})


@api_view(http_method_names=['POST'])
@permission_classes(IsAuthenticated)
def change_best_actor_vote(request):
    role_id = request.data('role_id')
    if not role_id:
        raise ParseError()

    try:
        role = Role.objects.get(role_id)
    except ObjectDoesNotExist:
        raise NotFound()

    watchlist_item = get_watchlist_item(request.user, role.movie)
    watchlist_item.best_actor = role
    watchlist_item.save()
    return Response({'status': 'Saved'})
