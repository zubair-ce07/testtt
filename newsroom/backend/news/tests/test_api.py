from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from backend.news.models import News, Newspaper, NewsSource
from backend.categories.models import Category
from backend.comments.models import Comment
from backend.users.models import User


class TestNewsViewSet(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='test category')
        cls.news_source = NewsSource.objects.create(name='unknown')
        cls.newspaper = Newspaper.objects.create(name='Dawn News',
                                                 source_url="https://www.dawn.com/")
        cls.new_item = News.objects.create(
            title='Test News',
            published_date='2017-09-05',
            source_url="https://www.dawn.com/test_news/",
            image_url="https://www.dawn.com/test_news/img",
            abstract='news abstract',
            detail='news detail',
            summary='news summary',
            news_source=cls.news_source,
            category=cls.category,
            newspaper=cls.newspaper
        )
        cls.user = User.objects.create(
            username='abcefg@gmail.com',
            first_name='test_first_name',
            last_name='test_last_name',
            email='abcefg@gmail.com'
        )
        cls.comment = Comment.objects.create(
            user=cls.user,
            news=cls.new_item,
            content='test comment',
        )

    def __set_client_credentials(self, user):
        token = Token.objects.get(user__username=user.username)
        token = 'Token {key}'.format(key=token.key)
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_get_top_news(self):
        response = self.client.get('/api/v1/news/top/')
        self.assertEqual(response.data[0]['title'],
                         self.new_item.title,
                         msg='get recent news'
                         )

    def test_get_news_categories(self):
        response = self.client.get('/api/v1/news/categories/')
        self.assertEqual(response.data[0]['title'],
                         self.new_item.title,
                         msg="get recent news of category 'test category'"
                         )

    def test_get_search_news(self):
        response = self.client.get(
            '/api/v1/news/search/?query={query}'.format(query='news')
        )
        self.assertEqual(response.data[0]['title'],
                         self.new_item.title,
                         msg="retrieve news by query 'news'"
                         )

    def test_get_news_comments(self):
        self.__set_client_credentials(self.user)
        response = self.client.get('/api/v1/news/{pk}/comments/'.format(pk=self.new_item.id))
        self.client.credentials()
        self.assertEqual(response.data[0]['content'],
                         self.comment.content,
                         msg="get comments of news with id '1'"
                         )

    def test_post_news_comment(self):
        self.__set_client_credentials(self.user)
        content = 'test comment 2'
        response = self.client.post('/api/v1/news/{pk}/comment/'.format(pk=self.new_item.id),
                                    {
                                        'content': content
                                    })
        self.client.credentials()
        self.assertEqual(response.data['content'],
                         content,
                         msg="post comment for news with id '1'"
                         )