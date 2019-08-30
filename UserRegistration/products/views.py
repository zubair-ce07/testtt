import json

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Product, Brand, Category, ProductArticle, ProductImage
from .serializers import ProductSerializer, BrandSerializer, CategorySerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        brand = request.POST['brand']
        category = request.POST['category']
        images = json.loads(request.POST['images'])
        articles = json.loads(request.POST['articles'])
        try:
            brand = Brand.objects.get(name=brand)
            category = Category.objects.get(name=category)
        except Brand.DoesNotExist:
            return Response({"not found": "brand not found"}, status=status.HTTP_404_NOT_FOUND)
        except Category.DoesNotExist:
            return Response({"not found": "category not found"}, status=status.HTTP_404_NOT_FOUND)
        with transaction.atomic():
            product, _ = Product.objects.get_or_create(
                name=request.POST['name'],
                brand=brand,
                category=category,
                description=request.POST['description']
            )
            self.save_images(product, images)
            self.save_articles(product, articles)
            serializer = ProductSerializer(product)
            return Response(serializer.data)

    @staticmethod
    def save_images(product, images):
        for image in images:
            ProductImage.objects.get_or_create(
                url=image['url'],
                product=product
            )

    @staticmethod
    def save_articles(product, articles):
        for article in articles:
            ProductArticle.objects.get_or_create(
                color=article['color'],
                price=article['price'],
                size=article['size'],
                product=product
            )


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

