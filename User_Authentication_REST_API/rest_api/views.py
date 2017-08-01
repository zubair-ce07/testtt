from django.http import Http404, HttpResponse
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from UserRegistration.models import User, Task
from .serializers import UsersTaskSerializer, RatingSerializer
from .serializers import UserSerializer, MovieSerializer, FavouritesSerializer, UserRatingSerializer
from cinescore.models import Movie, UserRating, Favorites, Rating


class UsersTaskListCreateView(generics.ListCreateAPIView):
    """
    View for creating and listing tasks for user

    Attributes:
        serializer_class: Being equal to UserTaskSerializer
        permission_classes: Permissions that would be checked before giving the response to the user
    """
    serializer_class = UsersTaskSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def perform_create(self, serializer):
        """
        Create task for incoming request user
        Note: The default perform_create() method is overwritten

        Args:
            serializer: The serializer that should be used
        """
        if self.request.user.is_superuser:
            user_id = self.request.POST.get('user')
            if user_id is not None:
                try:
                    User.objects.get(email=user_id)
                except User.DoesNotExist:
                    raise Http404('User Not Found')
                if serializer.is_valid():
                    serializer.save(user=User.objects.get(email=user_id))
                    return
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_superuser:
            return Task.objects.all().order_by('name')
        return Task.objects.filter(user=user)


class UserTaskDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    View to get, edit, and destroy given task
    """
    queryset = Task.objects.all()
    serializer_class = UsersTaskSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)


class CustomUserList(viewsets.ModelViewSet):
    """
    View for creating and listing users using inherited ModelViewSet

    Attributes:
        serializer_class: Being equal to UserTaskSerializer
        permission_classes: Permissions that would be checked before giving the response to the user
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class GetUpdateDeleteUserAPIView(APIView):
    """
    View to get, edit and destroy current user details

    Attributes:
        permission_classes: Permissions that would be checked before giving the response to the user
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Retrieve the requested user"""
        user = request.user
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    def patch(self, request):
        """Partially update the requested user's profile"""
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete the requested user"""
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request):
        """Completely update the requested user's profile"""
        user = request.user
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class RateMovieView(generics.ListCreateAPIView):
    serializer_class = UserRatingSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        rated_movies = UserRating.objects.filter(user=self.request.user)
        return UserRating.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        movie = Movie.objects.get(movie_id=request.POST['movie_id'])
        rating = request.POST['rating']
        user_rating = UserRating.objects.get(movie=movie, user=user)
        user_rating.rating = float(rating)
        user_rating.save()
        user_rating_serializer = UserRatingSerializer(user_rating)
        return Response(data=user_rating_serializer.data, status=status.HTTP_200_OK)


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


class FavoriteMoviesListView(generics.ListAPIView):
    serializer_class = FavouritesSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user)


class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = StandardResultsSetPagination


class RatingsListView(generics.ListAPIView):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    pagination_class = StandardResultsSetPagination
