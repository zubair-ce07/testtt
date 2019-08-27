from rest_framework import serializers

from .models import Product, ProductArticle, ProductImage


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductArticle
        fields = ['color', 'size', 'price']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['url']


class ProductSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'brand', 'images', 'articles']

