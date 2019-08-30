import json
from itertools import islice

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
            return Response({'not found': 'brand not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'not found': 'category not found'}, status=status.HTTP_400_BAD_REQUEST)
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
        batch_size = len(images)
        product_images = (ProductImage(url=image['url'], product=product) for image in images)
        batch = list(islice(product_images, batch_size))
        ProductImage.objects.bulk_create(batch, batch_size)

    @staticmethod
    def save_articles(product, articles):
        batch_size = len(articles)
        product_articles = (ProductArticle(
            color=article['color'],
            price=article['price'],
            size=article['size'],
            product=product
        ) for article in articles)
        batch = list(islice(product_articles, batch_size))
        ProductImage.objects.bulk_create(batch, batch_size)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

