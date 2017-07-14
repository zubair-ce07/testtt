from rest_framework import serializers
from super_store.models import Brand, Product, Images, Skus
from authentication.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name')


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('name', 'brand_link', 'image_icon', )


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ('product', 'image_url', )


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    image_product = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('brand', 'product_id', 'product_name',
                  'source_url', 'image_product')


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('brand', 'product_id', 'product_name',
                  'source_url',)


class SkuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skus
        fields = ('product', 'color', 'size', 'price', 'availability',)
