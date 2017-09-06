from rest_framework import serializers

from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'image', 'image_url', 'pub_date', 'publisher')

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        return obj.image_url
