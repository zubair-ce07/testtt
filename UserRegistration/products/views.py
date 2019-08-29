import json
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Product, Brand, Category, ProductArticle, ProductImage
from .serializers import ProductSerializer, BrandSerializer, CategorySerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        name = request.POST['name']
        description = request.POST['description']
        brand = request.POST['brand']
        category = request.POST['category']
        images = json.loads(request.POST['images'])
        articles = json.loads(request.POST['articles'])
        brand, _ = Brand.objects.get_or_create(name=brand)
        category, _ = Category.objects.get_or_create(name=category)
        product, _ = Product.objects.get_or_create(
            name=name,
            brand=brand,
            category=category,
            description=description
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

