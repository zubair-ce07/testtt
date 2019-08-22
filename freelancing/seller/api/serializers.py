from rest_framework import serializers

from ..models import Category, Gig, Gallery, Package


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'category_name')


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = (
            'id',
            'name',
            'details_offering',
            'delivery_time',
            'revisions',
            'price'
        )


class GigSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="category_name"
    )
    search_tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="search_tag"
    )
    seller = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Gig
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = (
            'id',
            'gig_image'
        )
