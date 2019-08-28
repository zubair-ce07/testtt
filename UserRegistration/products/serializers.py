from rest_framework import serializers

from .models import Product, ProductArticle, ProductImage, Brand, Category


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductArticle
        fields = ['color', 'size', 'price']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['url']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True)
    images = ImageSerializer(many=True)
    brand = BrandSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'brand', 'images', 'articles']

