import json
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from shopcity.models import Product
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase

from .serializers import ProductSerializer
from firstdjangoapp.urls import urlpatterns as base_urls


class ProductTestCase(TestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]
    urlpatterns += base_urls

    def setUp(self):
        Product.objects.create(
            retailer_sku="SS19-4000049209-BCK-10",
            name="Black seamless leggings",
            brand="NOVA",
            currency="GBP",
            price=600,
            url="https://www.isawitfirst.com/collections/trousers/products/seamless-leggings-black-jl36451",
            description="Black basic leggings with high waist and seamless design.;Model wears a S/UK 8 and her "
                        "height is 5'9\"",
            image_url="//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4000049209-BCK-1-022019-S2-isif_medium.jpg"
                      "?v=1555348106;//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4000049209-BCK-4-022019-S2"
                      "-isif_medium.jpg?v=1555348106;//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4000049209"
                      "-BCK-2-022019-S2-isif_medium.jpg?v=1555348106;//cdn.shopify.com/s/files/1/1962/2013/products"
                      "/SS19-4000049209-BCK-5-022019-S2-isif_medium.jpg?v=1555348106;//cdn.shopify.com/s/files/1/1962"
                      "/2013/products/SS19-4000049209-BCK-3-022019-S2-isif_medium.jpg?v=1555348107;//cdn.shopify.com"
                      "/s/files/1/1962/2013/t/12/assets/play.png?69541;//cdn.shopify.com/s/files/1/1962/2013/products"
                      "/SS19-4000049209-BCK-1-022019-S2-isif_medium.jpg?v=1555348106",
            care="",
            gender="women",
            out_of_stock=True
        )
        Product.objects.create(
            retailer_sku="SS19-4200057787-NNK-6",
            name="Neon pink wide trim bikini top",
            brand="SKETCH TRADING CO",
            currency="GBP",
            price=600,
            url="https://www.isawitfirst.com/collections/10-swimwear/products/wide-trim-bikini-top-bright-pink-jl44912",
            description="Neon pink bikini top with stripe band, triangle cups and cami straps.;Model wears a S/UK 8 "
                        "and her height is 5'9\"",
            image_url="//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4200057787-NNK-1-050919-IS2_medium.jpg?v"
                      "=1566581509;//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4200057787-NNK-145_medium.jpg"
                      "?v=1566581509;//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4200057789-NNK-2-050919"
                      "-IS2_medium.jpg?v=1566581509;//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4200057787"
                      "-NNK-5-050919-IS2_medium.jpg?v=1566581509;//cdn.shopify.com/s/files/1/1962/2013/products/SS19"
                      "-4200057787-NNK-4-050919-IS2_medium.jpg?v=1566581509",
            care="",
            gender="women",
            out_of_stock=False
        )
        self.valid_product_post_data = {
            "retailer_sku": "SS19-4200057787-NNK-600",
            "name": "Black Shirt",
            "brand": "Polo",
            "currency": "GBP",
            "price": 2000,
            "url": "https://www.isawitfirst.com/collections/10-swimwear/products/wide-trim-bikini-top-bright-pink"
                   "-jl44912",
            "description": "Black polo shirt",
            "image_url": "//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4200057787-NNK-1-050919-IS2_medium.jpg?v"
                         "=1566581509;//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4200057787-NNK-145_medium.jpg"
                         "?v=1566581509;//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4200057789-NNK-2-050919"
                         "-IS2_medium.jpg?v=1566581509;//cdn.shopify.com/s/files/1/1962/2013/products/SS19-4200057787"
                         "-NNK-5-050919-IS2_medium.jpg?v=1566581509;//cdn.shopify.com/s/files/1/1962/2013/products/SS19"
                         "-4200057787-NNK-4-050919-IS2_medium.jpg?v=1566581509",
            "care": "",
            "gender": "men",
            "out_of_stock": False
        }
        self.invalid_product_post_data = {
            "retailer_sku": "SS19-4200057787-NNK-6",
            "name": "",
            "brand": "",
            "currency": "",
            "price": 20,
            "url": "",
            "description": "Black polo shirt",
            "image_url": "",
            "care": "",
            "gender": "children",
            "out_of_stock": False
        }
        self.valid_update = {
            'out_of_stock': False
        }
        self.invalid_update = {
            'retailer_sku': 'SS19-4000049209-BCK-10'
        }
        self.user = User.objects.create(
            username='aadi',
            email='asad@gmail.com'
        )
        self.user.set_password('test12345')
        self.valid_user_post_data = {
            "profile": {
                "address": "Lahore",
                "city": "Lhe",
                "zip_code": 44000,
                "state": "punjab",
            },
            "password": "django",
            "is_superuser": True,
            "username": "asad",
            "email": "asad.ali@arbisoft.com",
        }

    def test_product_created(self):
        product = Product.objects.get(retailer_sku="SS19-4200057787-NNK-6")
        self.assertEqual(product.retailer_sku, "SS19-4200057787-NNK-6")

    def test_get_products(self):
        url = reverse('product_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_single_product(self):
        url = reverse(
            'product_detail',
            kwargs={'retailer_sku': 'SS19-4200057787-NNK-6'}
        )
        response = self.client.get(url, format='json')
        product = Product.objects.get(retailer_sku='SS19-4200057787-NNK-6')
        product = ProductSerializer(product).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, product)

    def test_get_single_invalid_product(self):
        url = reverse(
            'product_detail',
            kwargs={'retailer_sku': 'SS19-4200057787-NN1K-6'}
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_valid_products(self):
        url = reverse('product_list')
        params = {
            'Brand': 'SKETCH TRADING CO',
            'Out of Stock': False
        }
        response = self.client.get(
            url,
            params,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['brand'], 'SKETCH TRADING CO')

    def test_filter_invalid_products(self):
        url = reverse('product_list')
        params = {
            'Brand': 'SKETCH TRADING CO',
            'Out of Stock': True
        }
        response = self.client.get(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_filter_out_of_stock_products(self):
        url = reverse('product_list')
        params = {
            'Out of Stock': True
        }
        response = self.client.get(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_in_stock_products(self):
        url = reverse('product_list')
        params = {
            'Out of Stock': False
        }
        response = self.client.get(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_product(self):
        url = reverse(
            'product_detail',
            kwargs={'retailer_sku': 'SS19-4200057787-NNK-6'}
        )
        response = self.client.patch(
            url,
            data=json.dumps(self.valid_update),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_product(self):
        url = reverse(
            'product_detail',
            kwargs={'retailer_sku': 'SS19-4200057787-NNK-6'}
        )
        response = self.client.patch(
            url,
            data=json.dumps(self.invalid_update),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_valid_product(self):
        url = reverse('product_list')
        response = self.client.post(
            url,
            data=json.dumps(self.valid_product_post_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_product(self):
        url = reverse('product_list')
        response = self.client.post(
            url,
            data=json.dumps(self.invalid_product_post_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        url = reverse('product_list')
        response = self.client.post(
            url,
            data=json.dumps(self.valid_product_post_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse(
            'product_detail',
            kwargs={'retailer_sku': 'SS19-4200057787-NNK-600'}
        )
        product = Product.objects.filter(retailer_sku='SS19-4200057787-NNK-600')
        self.assertEqual(product.count(), 1)
        response = self.client.delete(url)
        product = Product.objects.filter(retailer_sku='SS19-4200057787-NNK-600')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(product.count(), 0)

    def test_delete_invalid_product(self):
        url = reverse(
            'product_detail',
            kwargs={'retailer_sku': 'SS19-4200057787-NNK-600'}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users(self):
        url = reverse('user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_single_valid_user(self):
        url = reverse(
            'user_detail',
            kwargs={'id': 1}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'aadi')

    def test_get_single_invalid_user(self):
        url = reverse(
            'user_detail',
            kwargs={'id': 2}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_valid_user(self):
        url = reverse('user_list')
        response = self.client.post(
            url,
            data=json.dumps(self.valid_user_post_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='asad')
        self.assertEqual(user.id, response.data['id'])

    def test_valid_user_token(self):
        url = reverse('token_obtain_pair')
        user = User.objects.get(username='aadi')
        user.set_password('test12345')
        user_credentials = {
            'username': 'aadi',
            'password': 'test12345'
        }
        response = self.client.post(
            url,
            json.dumps(user_credentials),
            content_type='application/json'
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_user_token(self):
        url = reverse('token_obtain_pair')
        user_credentials = {
            'username': 'asadali',
            'password': 'django'
        }
        response = self.client.post(
            url,
            json.dumps(user_credentials),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

