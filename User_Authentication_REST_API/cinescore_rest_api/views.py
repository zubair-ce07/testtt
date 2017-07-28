from requests import Response

from django.http import Http404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..cinescore.models import Movie, Category, Rating, Website, User, UserRating, Favorites
from .serializers import UserSerializer, MovieSerializer, RatingSerializer, FavouritesSerializer, \
                            UserRatingSerializer, CategorySerializer, WebsiteSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserList(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save()


class RateMovieView(generics.CreateAPIView):
    serializer_class = UserRatingSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        user = request.user
        movie = Movie.objects.get(movie_id=request.POST['movie_id'])
        rating = request.POST['rating']
        user_rating = UserRating.objects.create(rating=rating)
        user_rating.movie.add(movie)
        user_rating.user.add(user)


class FavoriteMoviesView(generics.CreateAPIView):
    serializer_class = FavouritesSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        user = request.user
        movie = Movie.objects.get(movie_id=request.POST['movie_id'])
        fav, created = Favorites.objects.get_or_create(user=user)
        fav.movies.add(movie)
        return Response(status=status.HTTP_201_CREATED)


class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = StandardResultsSetPagination
