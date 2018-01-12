from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

from user.fixtures.user_fixture import UserFixture
from grade.fixtures.grade_fixture import GradeFixture

from faker import Faker


class GradeTestCase(TestCase):
    
    def setUp(self):
        self.user_fixture = UserFixture()
        token = self.user_fixture.create_user_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.fake = Faker()
        self.grade_fixture = GradeFixture()
        
    def test_create_grade(self):
        
        data = self.grade_fixture.generate_data()

        response = self.client.post(
            reverse('grade-list'),
            data,
            format="json")

        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_grade(self):
        
        create_response = self.client.post(
            reverse('grade-list'),
            self.grade_fixture.generate_data(),
            format="json")

        data = self.grade_fixture.generate_data()
        updated_response = self.client.put(
            reverse('grade-detail', kwargs={'grade_id': create_response.data['id']}),
            data,
            format="json")
        
        self.assertEqual(updated_response.data['name'], data['name'])
        self.assertEqual(updated_response.status_code, status.HTTP_200_OK)
    
    def test_detail_grade(self):
        
        create_response = self.client.post(
            reverse('grade-list'),
            self.grade_fixture.generate_data(),
            format="json")

        response = self.client.get(
            reverse('grade-detail', kwargs={'grade_id': create_response.data['id']}),
            self.grade_fixture.generate_data(),
            format="json")
        
        self.assertEqual(response.data['name'], create_response.data['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_grade(self):
        total_insertions = 20
        for count in range(0,total_insertions):
            create_response = self.client.post(
                reverse('grade-list'),
                self.grade_fixture.generate_data(),
                format="json")
        
        response = self.client.get(
            reverse('grade-list'),
            format="json")
        
        self.assertEqual(total_insertions, len(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        