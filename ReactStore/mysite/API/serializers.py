from rest_framework import serializers
from super_store.models import Brand, Product, Images, Skus
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ('product', 'image_url', )


class SkuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skus
        fields = ('product', 'color', 'size', 'price', 'availability',)


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    skus_set = SkuSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('pk', 'product_id', 'product_name', 'category',
                  'source_url', 'images', 'skus_set')


class BrandOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('name', 'brand_link', 'image_icon')


class BrandSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ('pk', 'name', 'brand_link', 'image_icon', 'product')
        read_only_fields = ('pk',)
