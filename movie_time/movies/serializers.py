from rest_framework import serializers
from movies.models import Movie, Genre, Image, Video, Person, Role, Job
from watchlists.models import WatchListItem


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['key', 'site', 'name', 'size', 'type', 'iso_639_1', 'iso_3166_1']


class ImageSerializer(serializers.ModelSerializer):
    def get_image_type(self, image):
        return image.get_type_display()

    image_type = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['aspect_ratio', 'file_path', 'height', 'width',
                  'iso_639_1', 'vote_average', 'vote_count', 'image_type']


class PersonSerializer(serializers.ModelSerializer):
    def get_gender(self, person):
        return person.get_gender_display()

    def get_profile(self, person):
        images = person.images.all()
        if images:
            max_vote_avg_profile = images[0]

            for image in images[1:]:
                if image.vote_average > max_vote_avg_profile.vote_average:
                    max_vote_avg_profile = image
            return max_vote_avg_profile.file_path if max_vote_avg_profile else None

    gender = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['gender', 'tmdb_id', 'name', 'profile']


class RoleSerializer(serializers.ModelSerializer):
    def get_votes(self, role):
        return len(role.votes.all())

    person = PersonSerializer()
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'character', 'order', 'person', 'votes']


class JobSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Job
        fields = ['id', 'department', 'job', 'person']


class WatchListItemSerializer(serializers.ModelSerializer):
    def get_rating(self, watchlist_item):
        return watchlist_item.get_rating_display()

    rating = serializers.SerializerMethodField()

    class Meta:
        model = WatchListItem
        fields = ['movie', 'is_watched', 'is_recommended', 'removed', 'best_actor', 'rating']


class MetaMovieSerializer(serializers.ModelSerializer):
    def get_max_vote_avg_images(self, movie):
        max_vote_avg_for_poster = -1
        max_vote_avg_for_backdrop = -1
        best_backdrop = None
        best_poster = None

        for image in movie.images.all():
            if image.type == Image.POSTER:
                if image.vote_average > max_vote_avg_for_poster:
                    best_poster = image
                    max_vote_avg_for_poster = image.vote_average
            elif image.type == Image.BACKDROP:
                if image.vote_average > max_vote_avg_for_backdrop:
                    best_backdrop = image
                    max_vote_avg_for_backdrop = image.vote_average

        return best_poster, best_backdrop

    def get_max_voted_images(self, movie):
        best_poster, best_backdrop = self.get_max_vote_avg_images(movie)
        poster_path = best_poster.file_path if best_poster else None
        backdrop_path = best_backdrop.file_path if best_backdrop else None
        return {'poster': poster_path, 'backdrop': backdrop_path}

    def get_user_statuses(self, movie):
        request = self.context.get('request')
        if request and not request.user.is_anonymous:
            for watchlist_item in movie.watchlist_items.all():
                if watchlist_item.user.id is request.user.id:
                    return WatchListItemSerializer(watchlist_item).data if watchlist_item else None

    @staticmethod
    def get_counts(movie):
        add_count, watched_count, recommended_count, like_count, dislikes_count = (0, 0, 0, 0, 0)
        for watchlist_item in movie.watchlist_items.all():
            if not watchlist_item.removed:
                add_count += 1
            if watchlist_item.is_watched:
                watched_count += 1
            if watchlist_item.is_recommended:
                recommended_count += 1
            if watchlist_item.rating == WatchListItem.LIKED:
                like_count += 1
            elif watchlist_item.rating == WatchListItem.DISLIKED:
                dislikes_count += 1
        return {
            'added': add_count, 'watched': watched_count, 'recommended': recommended_count,
            'likes': like_count, 'dislikes': dislikes_count
        }

    genres = GenreSerializer(many=True)
    release_date = serializers.StringRelatedField()
    max_voted_images = serializers.SerializerMethodField()
    user_statuses = serializers.SerializerMethodField()
    counts = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'counts', 'overview', 'release_date', 'max_voted_images', 'status',
                  'title', 'vote_average', 'vote_count', 'genres', 'user_statuses']


class MovieSerializer(MetaMovieSerializer, serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(MovieSerializer, self).__init__(*args, **kwargs)
        fields = self.context.get('include')

        if fields:
            fields = fields.split(',')
            if 'cast' in fields:
                self.fields['cast'] = RoleSerializer(source='role_set', many=True)
            if 'crew' in fields:
                self.fields['crew'] = JobSerializer(source='job_set', many=True)
            if 'videos' in fields:
                self.fields['videos'] = VideoSerializer(many=True)
            if 'images' in fields:
                self.fields['images'] = ImageSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'adult', 'counts', 'budget', 'homepage', 'original_language', 'original_title', 'overview',
                  'popularity', 'release_date', 'max_voted_images', 'revenue', 'runtime', 'status', 'tag_line', 'title',
                  'vote_average', 'vote_count', 'genres', 'user_statuses']
