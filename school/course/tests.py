from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

from user.fixtures.user_fixture import UserFixture
from course.fixtures.course_fixture import CourseFixture

from faker import Faker


class CourseTestCase(TestCase):
    
    def setUp(self):
        self.user_fixture = UserFixture()
        token = self.user_fixture.create_user_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.fake = Faker()
        self.course_fixture = CourseFixture()
        
    def test_create_course(self):
        
        response = self.client.post(
            reverse('course-list'),
            self.course_fixture.generate_data(),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_course(self):
        
        create_response = self.client.post(
            reverse('course-list'),
            self.course_fixture.generate_data(),
            format="json")

        update_response = self.client.put(
            reverse('course-detail', kwargs={'course_id': create_response.data['id']}),
            self.course_fixture.generate_data(),
            format="json")
            
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
    
    def test_detail_course(self):
        
        create_response = self.client.post(
            reverse('course-list'),
            self.course_fixture.generate_data(),
            format="json")

        response = self.client.get(
            reverse('course-detail', kwargs={'course_id': create_response.data['id']}),
            self.course_fixture.generate_data(),
            format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_course(self):

        for count in range(0,20):
            create_response = self.client.post(
                reverse('course-list'),
                self.course_fixture.generate_data(),
                format="json")
        
        response = self.client.get(
            reverse('course-list'),
            format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        