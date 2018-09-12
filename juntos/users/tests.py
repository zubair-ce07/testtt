from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse
from ddt import ddt, data, unpack

from .models import Profile


@ddt
class UserFormViewTest(TestCase):
    """
    Test user form view test.
    """
    def setUp(self):
        """
        Setting up a user and a profile to login user
        """
        user = User.objects.create(
            username='test', email='test@gmail.com',
            first_name='mad', last_name='math'
        )
        user.set_password('12345')
        user.save()

        Group.objects.create(name='Admin')

    def test_registration_get(self):
        """
        Test Registration get view.
        """
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'],  reverse('users:register'))

    def test_registration_post_valid_info(self):
        """
        A `POST` to the `register` view with valid data properly
        creates a new user and issues a redirect.
        """
        data = {
            'username': 'admin',
            'password': 'youcanthackit',
            'email': 'admin@gmail.com',
            'first_name': 'mad',
            'last_name': 'math',
            'role': '1'
        }
        response = self.client.post(reverse('users:register'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.context, None)
        self.assertEqual(response.url, '/')
        self.assertRedirects(response, reverse('users:index'))

    @data(
        {
            'username': 'admin',
            'password': 'youcanthackit',
            'email': 'admin@gmail.com',
            'first_name': '',
            'last_name': 'math',
            'error': {'field': 'first_name', 'desc': 'First name is required.'}
        },
        {
            'username': 'admin',
            'password': 'youcanthackit',
            'email': 'admin@gmail.com',
            'first_name': 'mad',
            'last_name': '',
            'error': {'field': 'last_name', 'desc': 'Last name is required.'}
        },
        {
            'username': 'admin',
            'password': 'youcanthackit',
            'email': '',
            'first_name': 'mad',
            'last_name': 'math',
            'error': {'field': 'email', 'desc': 'Enter a valid email'}
        },
        {
            'username': 'admin',
            'password': 'youcanthackit',
            'email': '123@132',
            'first_name': 'mad',
            'last_name': 'math',
            'error': {'field': 'email', 'desc': 'Enter a valid email address.'}
        },
        {
            'username': '',
            'password': 'youcanthackit',
            'email': 'admin@gmail.com',
            'first_name': 'mad',
            'last_name': 'math',
            'error': {'field': 'username', 'desc': 'This field is required.'}
        },
        {
            'username': 'test',
            'password': 'youcanthackit',
            'email': 'admin@gmail.com',
            'first_name': 'mad',
            'last_name': 'math',
            'error': {'field': 'username', 'desc': 'A user with that username already exists.'}
        },
        {
            'username': 'admin',
            'password': 'youcanthackit',
            'email': 'test@gmail.com',
            'first_name': 'mad',
            'last_name': 'math',
            'error': {'field': 'email', 'desc': 'Email already exists'}
        }
    )
    @unpack
    def test_registration_post_w_invalid_data(self, username, password, email, first_name, last_name, error):
        """
        A `POST` to the `register` view with invalid information does not
        creates a new user and returns error.
        """

        response = self.client.post(reverse('users:register'), data={
            'username': username,
            'password': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('users:register'))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=error['field'], errors=error['desc'])


class IndexDetailViewTest(TestCase):
    """
    Test index detail view
    """
    def setUp(self):
        """
        Setting up a user and a profile to login user
        """
        user = User.objects.create(
            username='test', email='test@gmail.com',
            first_name='mad', last_name='math'
        )
        user.set_password('12345')
        user.save()

    def test_without_login(self):
        """
        A `get` to the `index` view without `logged in` user does not
        takes to `index` rather redirects to `login`.
        """
        response = self.client.get(reverse('users:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('users:login')}?next=/")
        self.assertEqual(response.context, None)

    def test_with_login(self):
        """
        A `get` to the `index` view with `logged in` user does
        takes to `index`.
        """
        self.client.login(username='test', password='12345')
        response = self.client.get(reverse('users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('users:index'))
        self.assertTemplateUsed(response, 'profile/index.html')
        self.assertContains(response, 'Welcome test')

    def test_login_with_already_login(self):
        """
        A `get` to the `login` view with`logged in` user does not
        takes to `login` rather redirects to `index`.
        """
        self.client.login(username='test', password='12345')
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:index'))

    def test_register_with_already_login(self):
        """
        A `get` to the `register` view with`logged in` user does not
        takes to `register` rather redirects to `index`.
        """
        self.client.login(username='test', password='12345')
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:index'))


class ProfileUpdateTest(TestCase):
    """
    Test profile update view
    """
    def setUp(self):
        """
        Setting up a user and a profile to login user
        """
        user = User.objects.create(
            username='test', email='test@gmail.com',
            first_name='mad', last_name='math'
        )
        user.set_password('12345')
        user.save()

    def test_get_without_login(self):
        """
        A `get` to the `edit_profile` view without `logged in` user does not
        takes to `edit_profile` rather redirects to `login`.
        """
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('users:edit_profile')}")
        self.assertEqual(response.context, None)

    def test_get_with_login(self):
        """
        A `get` to the `edit_profile` view with `logged in` user does
        takes to `edit_profile`.
        """
        self.client.login(username='test', password='12345')
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('users:edit_profile'))
        self.assertTemplateUsed(response, 'profile/generic_form.html')
        self.assertIn('profile', response.context)  # Testing Model for which form is generated by Generic View.

    def test_post_without_login(self):
        """
        A `post` to the `edit_profile` view without `logged in` user does not
        takes to `edit_profile` rather redirects to `login`.
        """
        data = {
            'address': 'Mars',
            'age': 1,
            'profile_photo': '',
            'gender': 'M'
        }
        response = self.client.post(reverse('users:edit_profile'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('users:edit_profile')}")
        self.assertEqual(response.context, None)

    def test_post_with_login_valid_info(self):
        """
        A `post` to the `edit_profile` view with `logged in` user and valid information does
        takes to `index` and also changes information.
        """
        data = {
            'address': 'Mars',
            'age': 1,
            'profile_photo': '',
            'gender': 'M'
        }
        self.client.login(username='test', password='12345')
        response = self.client.post(reverse('users:edit_profile'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:index'))

        profile = Profile.objects.get(pk=1)
        self.assertEqual(profile.address, 'Mars')
        self.assertEqual(profile.age, 1)
        self.assertEqual(profile.profile_photo, '')
        self.assertEqual(profile.gender, 'M')

    def test_post_with_login_invalid_info(self):
        """
        A `post` to the `edit_profile` view with `logged in` user and invalid information does not
        takes to `index` and returns error.
        """
        data = {
            'address': 'Mars',
            'age': -1,
            'profile_photo': '',
            'gender': 'M'
        }
        self.client.login(username='test', password='12345')
        response = self.client.post(reverse('users:edit_profile'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('users:edit_profile'))
        self.assertFormError(response, 'form', field=None, errors='Age must be positive')


@ddt
class UserUpdateTest(TestCase):
    """
    Test user update
    """
    def setUp(self):
        """
        Setting up two users to test duplicate email Validation.
        """
        user = User.objects.create(
            username='test', email='test@gmail.com',
            first_name='mad', last_name='math'
        )
        user.set_password('12345')
        user.save()
        user = User.objects.create(
            username='test1', email='to_test_duplicate_email@gmail.com',
            first_name='mad1', last_name='math1'
        )
        user.set_password('12345')
        user.save()

        Group.objects.create(name='Admin')

    def test_get_without_login(self):
        """
        A `get` to the `edit_basic_info` view without `logged in` user does not
        takes to `edit_basic_info` rather redirects to `login`.
        """
        response = self.client.get(reverse('users:edit_basic_info'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('users:edit_basic_info')}")
        self.assertEqual(response.context, None)

    def test_get_with_login(self):
        """
        A `get` to the `edit_basic_info` view without `logged in` user does
        takes to `edit_basic_info`.
        """
        self.client.login(username='test', password='12345')
        response = self.client.get(reverse('users:edit_basic_info'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('users:edit_basic_info'))
        self.assertTemplateUsed(response, 'profile/generic_form.html')
        self.assertIn('user', response.context)  # Testing Model for which form is generated by Generic View.

    def test_post_without_login(self):
        """
        A `post` to the `edit_basic_info` view without `logged in` user does not
        takes to `edit_basic_info` rather redirects to `login`.
        """
        data = {
            'email': 'admin@gmail.com',
            'first_name': 'mad',
            'last_name': 'math',
            'username': 'test',
            'password': '12345'
        }
        response = self.client.post(reverse('users:edit_basic_info'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('users:edit_basic_info')}")
        self.assertEqual(response.context, None)

    def test_post_with_login_valid_info(self):
        """
        A `post` to the `edit_basic_info` view with `logged in` user and valid information does
        takes to `index` and also changes information.
        """
        data = {
            'email': 'admin@gmail.com',
            'first_name': 'math',
            'last_name': 'fan',
            'username': 'test',
            'role': '1',
            'password': '12345'
        }
        self.client.login(username='test', password='12345')
        response = self.client.post(reverse('users:edit_basic_info'), data=data)
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(pk=1)
        self.assertEqual(user.email, 'admin@gmail.com')
        self.assertEqual(user.first_name, 'math')
        self.assertEqual(user.last_name, 'fan')

    @data(
        {
            'email': 'to_test_duplicate_email@gmail.com',
            'first_name': 'math',
            'last_name': 'fan',
            'username': 'test',
            'password': '12345',
            'error': {'field': 'email', 'desc': 'Email already exists'}
        },
        {
            'email': 'a12#ad@s.d',
            'first_name': 'math',
            'last_name': 'fan',
            'username': 'test',
            'password': '12345',
            'error': {'field': 'email', 'desc': 'Enter a valid email address.'}
        },
        {
            'email': 'admin@gmail.com',
            'first_name': '',
            'last_name': 'fan',
            'username': 'test',
            'password': '12345',
            'error': {'field': 'first_name', 'desc': 'First name is required.'}
        },
        {
            'email': 'admin@gmail.com',
            'first_name': 'math',
            'last_name': '',
            'username': 'test',
            'password': '12345',
            'error': {'field': 'last_name', 'desc': 'Last name is required.'}
        },
    )
    @unpack
    def test_post_with_login_w_invalid_info(self, email, first_name, last_name, username, password, error):
        """
        A `post` to the `edit_basic_info` view with `logged in` user and invalid information does not
        takes to `index` and returns error.
        """
        self.client.login(username='test', password='12345')
        response = self.client.post(reverse('users:edit_basic_info'), data={
            'username': username,
            'password': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('users:edit_basic_info'))
        self.assertFormError(response, 'form', field=error['field'], errors=error['desc'])
