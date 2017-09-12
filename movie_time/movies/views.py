from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from nltk.corpus import stopwords
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from movies.serializers import MovieSerializer, MetaMovieSerializer, GenreSerializer
from movies.models import Date, Movie, Genre


@api_view(http_method_names=['GET'])
def get_movie(request, pk):
    return Response(MovieSerializer(
        Movie.objects.select_related(
            'release_date').prefetch_related('videos', 'images', 'role_set__person__images', 'role_set__votes',
                                             'job_set__person__images', 'genres', 'watchlist_items').get(id=pk),
        context={'include': request.query_params.get('include'), 'request': request}
    ).data)


@api_view(http_method_names=['GET'])
def search_movies(request):
    search_string = request.GET.get('q', "")
    if not search_string:
        raise ParseError

    filtered_words = [word.lower() for word in search_string.split() if word.lower() not in stopwords.words('english')]

    queries = [Q(title__icontains=keyword) for keyword in filtered_words]
    query = queries.pop()
    for condition in queries:
        query |= condition
    search_results = Movie.objects.filter(query).order_by('-popularity').select_related(
        'release_date').prefetch_related('genres', 'images', 'watchlist_items')[:10]

    serializer = MetaMovieSerializer(
        search_results,
        many=True,
        context={'request': request}
    )

    data = serializer.data
    return Response(data=data)


class GetGenresMovies(ListAPIView):
    serializer_class = MetaMovieSerializer

    def get_queryset(self):
        try:
            genre = Genre.objects.get(id=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            raise NotFound()

        return Movie.objects.filter(genres=genre).order_by('-popularity').select_related(
            'release_date').prefetch_related('genres', 'images', 'watchlist_items')


class GetGenres(ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class GetMoviesReleasedOnDate(ListAPIView):
    serializer_class = MetaMovieSerializer

    def get_queryset(self):
        day = self.request.GET.get('day')
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')

        if not (day and month and year):
            raise ParseError()

        released_dates = Date.objects.filter(day=day, month=month, year=year)
        return Movie.objects.filter(release_date__in=released_dates).order_by('-popularity').select_related(
            'release_date').prefetch_related('genres', 'images', 'watchlist_items')
