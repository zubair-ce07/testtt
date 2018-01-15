from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

from user.fixtures.user_fixture import UserFixture
from lms.fixtures.lms_fixture import AuthorFixture, BookFixture

from faker import Faker


class AuthorTestCase(TestCase):
    
    def setUp(self):
        self.user_fixture = UserFixture()
        token = self.user_fixture.create_user_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.fake = Faker()
        self.author_fixture = AuthorFixture()
        
    def test_create_author(self):
        
        data = self.author_fixture.generate_data()

        response = self.client.post(
            reverse('author-list'),
            data,
            format="json")
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
class BookTestCase(TestCase):
    
    def setUp(self):
        self.user_fixture = UserFixture()
        token = self.user_fixture.create_user_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.fake = Faker()
        self.author_fixture = AuthorFixture()
        self.book_fixture = BookFixture()
    
    def create_book_authors(self):
        
        total_authors = 4

        data = self.author_fixture.generate_data()
        
        response = []
        
        for count in range(0,total_authors):
            author = self.client.post(
                reverse('author-list'),
                data,
                format="json")

            response.append(author.data['id']) 
        
        return response

    def test_create_author(self):

        authors = self.create_book_authors()
        
        data = self.book_fixture.generate_data()

        data['authors'] = authors
        
        response = self.client.post(
            reverse('book-list'),
            data,
            format="json")
        
        result = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            [result['title'], result['description'], result['summary'], result['authors']],
            [data['title'], data['description'], data['summary'], authors]
        )
    
    def test_update_author(self):

        authors = self.create_book_authors()
        
        data = self.book_fixture.generate_data()

        data['authors'] = authors
        
        response = self.client.post(
            reverse('book-list'),
            data,
            format="json")
        
        book_created = response.data
        
        response = self.client.put(
            reverse('book-detail', kwargs={'book_id': book_created['id']}),
            data,
            format="json")

        result = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [result['title'], result['description'], result['summary'], result['authors']],
            [data['title'], data['description'], data['summary'], authors]
        )

        
    
    