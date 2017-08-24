from rest_framework.viewsets import ModelViewSet
from reviews.serializers import ReviewSerializer, Review


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(movie_id=self.kwargs['movie_id'])
