from rest_framework import serializers

from accounts.models import User
from ..models import Category, Gig, Gallery, \
    Package, Faq, Requirements

from dashboard.models import Offers, Requests


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
            'price',
            'gig'
        )


class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = '__all__'


class RequirementsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requirements
        fields = '__all__'


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
        queryset=User.objects.all()
    )
    gig_packages = PackageSerializer(read_only=True, many=True)
    gig_faqs = FaqSerializer(read_only=True, many=True)
    gig_requirements = RequirementsSerializer(read_only=True, many=True)

    class Meta:
        model = Gig
        fields = (
            'id',
            'seller',
            'search_tags',
            'categories',
            'gig_title',
            'gig_packages',
            'gig_faqs',
            'gig_requirements'
        )


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = (
            'id',
            'gig_image',
            'gig'
        )


class OfferSerializer(serializers.ModelSerializer):

    seller = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    buyer_request = serializers.PrimaryKeyRelatedField(
        queryset=Requests.objects.all()
    )

    class Meta:
        model = Offers
        fields = (
            'id',
            'description',
            'offer_amount',
            'delivery_time',
            'revisions',
            'seller',
            'buyer_request'
        )
