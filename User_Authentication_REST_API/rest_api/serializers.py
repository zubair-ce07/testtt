from rest_framework import serializers

from UserRegistration.models import User, Task
from cinescore.models import Movie, Category, Rating, Website, UserRating, Favorites


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_superuser']
        read_only_fields = ('is_superuser',)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UsersTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task Model

    Task model fields are used where user attribute is specified implicitly
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'dated', 'user']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['category_name']


class MovieSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ['movie_id', 'title', 'category', 'date_of_release', 'poster', 'content_rating', 'plot']


class WebsiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Website
        fields = ['url', 'name']


class RatingSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    provider_website = WebsiteSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['movie', 'provider_website', 'rating', 'target_url']


class UserRatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = UserRating
        fields = ['user', 'movie', 'rating']


class FavouritesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movies = MovieSerializer(many=True)

    class Meta:
        model = Favorites
        fields = ['user', 'movies']