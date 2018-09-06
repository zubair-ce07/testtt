from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from learnerapp import serializers
from learnerapp.tests import testdata

user_data = {'username': 'zainabteacher', 'first_name': 'Zainab',
             'last_name': 'Amir', 'email': 'zainab.amir@arbisoft.com'}


class CreateUserTest(APITestCase):
    def setUp(self):
        user, student = testdata.create_student(testdata.user_data)
        self.client.force_login(user)

    def test_can_create_instructor(self):
        response = self.client.post(reverse('instructor-list'), testdata.post_instructor)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_create_student(self):
        response = self.client.post(reverse('student-list'), testdata.post_student)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CreateCourseTest(APITestCase):
    def setUp(self):
        user, student = testdata.create_student(testdata.user_data)
        self.client.force_login(user)

    def test_can_create_course(self):
        response = self.client.post(reverse('course-list'), testdata.post_course)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReadAPITest(APITestCase):
    def setUp(self):
        user, self.student = testdata.create_student(testdata.user_data)
        self.client.force_login(user)

    def test_can_read_student_list(self):
        response = self.client.get(reverse('student-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_details(self):
        response = self.client.get(reverse('student-detail', args=[self.student.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_instructor_list(self):
        response = self.client.get(reverse('instructor-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_read_course_list(self):
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StudentUpdateTest(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()
        request = factory.post('/student/create/', {})

        user, self.student = testdata.create_student(testdata.user_data)
        self.client.force_login(user)
        self.data = serializers.StudentSerializer(self.student, context={'request': request}).data
        self.data.update({'first_name': 'Changed'})

    def test_can_update_user(self):
        response = self.client.put(reverse('student-detail', args=[self.student.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InstructorUpdateTest(APITestCase):
    def setUp(self):
        user, student = testdata.create_student(testdata.user_data)
        self.client.force_login(user)
        factory = APIRequestFactory()
        request = factory.post('/instructor/create/', {})
        instructor_credentials, self.instructor = testdata.create_instructor(user_data)
        self.data = serializers.InstructorSerializer(self.instructor, context={'request': request}).data
        self.data.update({'first_name': 'Changed'})

    def test_can_update_user(self):
        response = self.client.put(reverse('instructor-detail', args=[self.instructor.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteUserTest(APITestCase):
    def setUp(self):
        self.student_credentials, student = testdata.create_student(testdata.user_data)
        self.client.force_login(self.student_credentials)
        self.instructor_credentials, instructor = testdata.create_instructor(user_data)

    def test_can_delete_instructor(self):
        response = self.client.delete(reverse('instructor-detail', args=[self.instructor_credentials.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_student(self):
        response = self.client.delete(reverse('student-detail', args=[self.student_credentials.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)