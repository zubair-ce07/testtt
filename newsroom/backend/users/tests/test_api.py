from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from backend.categories.models import Category
from backend.users.models import User, UserInterest


class TestUserAPIView(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='test category')
        cls.user = User.objects.create(
            username='abcefg@gmail.com',
            first_name='test_first_name',
            last_name='test_last_name',
            email='abcefg@gmail.com'
        )
        cls.user.set_password('user12345')
        cls.user.save()
        cls.user_interests = UserInterest.objects.create(
            user=cls.user,
            category=cls.category
        )

    def __set_client_credentials(self, user):
        token = Token.objects.get(user__username=user.username)
        token = 'Token {key}'.format(key=token.key)
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_user_authenticate(self):
        response = self.client.post('/api/v1/users/authenticate/',
                         {
                             'username': self.user.username,
                             'password': 'user12345'
                         }
                         )
        token = Token.objects.get(user__username=self.user.username)
        self.assertEqual(response.data['token'],
                         token.key,
                         msg='user authentication to get token'
                         )
    def test_user_get_interests(self):
        self.__set_client_credentials(self.user)
        response = self.client.get('/api/v1/users/interests/')
        self.client.credentials()
        self.assertEqual(response.data[0]['category']['name'],
                         self.user_interests.category.name,
                         msg='get user interests'
                         )

    def test_user_update_interests(self):
        user_interest = Category.objects.create(name='test category 2')
        self.__set_client_credentials(self.user)
        response = self.client.post('/api/v1/users/interests/',
                                   {
                                       'interests': [user_interest.name]
                                   })
        self.client.credentials()
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         msg='update user interests'
                         )

    def test_user_create(self):
        email = 'qwerty@gmail.com'
        first_name = 'test_first_name_2'
        last_name = 'test_last_name_2'
        password = 'user12345'
        response = self.client.post('/api/v1/users/create/',
                         {
                            'email': email,
                            'username': email,
                            'first_name': first_name,
                            'last_name': last_name,
                            'password': password
                         })
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         msg='creating user'
                         )

    def test_user_get_profile(self):
        self.__set_client_credentials(self.user)
        response = self.client.get('/api/v1/users/profile/')
        self.client.credentials()
        self.assertEqual(response.data['username'],
                         self.user.username,
                         msg='get user profile'
                         )

    def test_user_update_profile(self):
        self.__set_client_credentials(self.user)
        first_name = 'test_first_name_changed'
        response = self.client.post('/api/v1/users/profile/',
                                    {
                                        'username': self.user.username,
                                        'email': self.user.email,
                                        'first_name': first_name,
                                        'last_name': self.user.last_name
                                    })
        self.client.credentials()
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         msg="update user's first name"
                         )
