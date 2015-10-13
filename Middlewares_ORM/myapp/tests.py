from django.contrib.auth.models import User
from django.test import TestCase
from ddt import ddt, data, unpack

@ddt
class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='test1', password='test1', email='test1@test.com')
        User.objects.create(username='test2', password='test2', email='test2@test.com')

    @unpack
    @data({'password': 'test1', 'email': 'test1@test.com'},
          {'password': 'test2', 'email': 'test2@test.com'})
    def test_login(self, password, email):
        self.client.login(email=email, password=password)
        user = User.objects.get(email=email)
        self.assertTrue(user.is_authenticated())
