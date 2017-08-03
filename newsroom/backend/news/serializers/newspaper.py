from rest_framework.serializers import ModelSerializer
from backend.news.models import Newspaper


class NewspaperSerializer(ModelSerializer):

    class Meta:
        model = Newspaper
        fields = ('id', 'name', 'source_url', )