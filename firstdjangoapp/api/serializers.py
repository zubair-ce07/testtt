from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from shopcity.models import Category, Product, Skus
from users.models import Cart, CartItem, Profile


class SkusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skus
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category']


class ProductSerializer(serializers.ModelSerializer):
    skus = SkusSerializer(many=True, required=False, read_only=True)
    category = CategorySerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, required=False)
    cart = CartSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user
