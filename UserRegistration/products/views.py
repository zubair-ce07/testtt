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
            return Response({'error': 'invalid brand'}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'error': 'invalid category'}, status=status.HTTP_400_BAD_REQUEST)
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
        product_images = (ProductImage(url=image['url'], product=product) for image in images)
        ProductImage.objects.bulk_create(product_images)

    @staticmethod
    def save_articles(product, articles):
        product_articles = (ProductArticle(
            color=article['color'],
            price=article['price'],
            size=article['size'],
            product=product
        ) for article in articles)
        ProductImage.objects.bulk_create(product_articles)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

