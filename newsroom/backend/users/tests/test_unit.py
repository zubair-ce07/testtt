from django.test import SimpleTestCase
from rest_framework.test import force_authenticate
from backend.users.models import User, UserInterest
from backend.categories.models import Category
from backend.users.serializers.user import UserSerializer
from backend.users.serializers.interest import UserInterestSerializer

user = User(
    id=1,
    username='abc@gmail.com',
    email='abc@gmail.com',
    first_name='test',
    last_name='user'
    )

categories = [
    Category(
            id=1,
            name='test category 1'
        ),
    Category(
            id=2,
            name='test category 2'
        )
]

user_interests = [
    UserInterest(
        user=user,
        category=categories[0]
    ),
    UserInterest(
        user=user,
        category=categories[1]
    )
]


class TestUser(SimpleTestCase):
    def test_user_serializer_with_values(self):
        serialized_user = UserSerializer(user).data
        self.assertEqual(serialized_user['id'], user.id)
        self.assertEqual(serialized_user['username'], user.username)
        self.assertEqual(serialized_user['email'], user.email)
        self.assertEqual(serialized_user['first_name'], user.first_name)
        self.assertEqual(serialized_user['last_name'], user.last_name)

    def test_user_serializer_with_empty_values(self):
        serialized_user = UserSerializer(User()).data
        self.assertEqual(serialized_user['id'], None)
        self.assertEqual(serialized_user['username'], '')
        self.assertEqual(serialized_user['email'], '')
        self.assertEqual(serialized_user['first_name'], '')
        self.assertEqual(serialized_user['last_name'], '')

    def test_user_interest_serializer_with_values(self):
        serialized_user_interests = UserInterestSerializer(user_interests, many=True).data

        for i in range(len(user_interests)):
            self.assertEqual(serialized_user_interests[i]['category']['id'], user_interests[i].category.id)
            self.assertEqual(serialized_user_interests[i]['category']['name'], user_interests[i].category.name)

    def test_user_interest_serializer_with_empty_values(self):
        interests = [UserInterest()]
        serialized_user_interests = UserInterestSerializer(interests, many=True).data
        for i in range(len(interests)):
            self.assertIsNone(serialized_user_interests[i]['category'])

    def test_user_interest_serializer_with_empty_list(self):
        serialized_user_interests = UserInterestSerializer([], many=True).data

        self.assertEqual(serialized_user_interests, [])