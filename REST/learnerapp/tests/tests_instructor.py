from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from learnerapp import serializers
from learnerapp.tests import testdata

user_data = {'username': 'zainabteacher', 'first_name': 'Zainab',
             'last_name': 'Amir', 'email': 'zainab.amir@arbisoft.com'}


class CreateUserTest(APITestCase):
    def setUp(self):
        user, instructor = testdata.create_instructor(testdata.user_data)
        self.client.force_login(user)

    def test_can_create_instructor(self):
        response = self.client.post(reverse('instructor-list'), testdata.post_instructor)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_student(self):
        response = self.client.post(reverse('student-list'), testdata.post_student)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CreateCourseTest(APITestCase):
    def setUp(self):
        user, instructor = testdata.create_instructor(testdata.user_data)
        self.client.force_login(user)

    def test_can_create_course(self):
        response = self.client.post(reverse('course-list'), testdata.post_course)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadAPITest(APITestCase):
    def setUp(self):
        student_credentials, self.student = testdata.create_student(testdata.user_data)
        user, instructor = testdata.create_instructor(user_data)
        self.client.force_login(user)

    def test_can_read_student_list(self):
        response = self.client.get(reverse('student-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_details(self):
        response = self.client.get(reverse('student-detail', args=[self.student.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_instructor_list(self):
        response = self.client.get(reverse('instructor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_course_list(self):
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InstructorUpdateTest(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()
        request = factory.post('/instructor/create/', {})

        user, self.instructor = testdata.create_instructor(user_data)
        self.client.force_login(user)
        self.data = serializers.InstructorSerializer(self.instructor, context={'request': request}).data
        self.data.update({'first_name': 'Changed'})

    def test_can_update_user(self):
        response = self.client.put(reverse('instructor-detail', args=[self.instructor.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StudentUpdateTest(APITestCase):
    def setUp(self):
        user, instructor = testdata.create_instructor(user_data)
        self.client.force_login(user)
        factory = APIRequestFactory()
        request = factory.post('/student/create/', {})
        student_credentials, self.student = testdata.create_student(testdata.user_data)
        self.data = serializers.StudentSerializer(self.student, context={'request': request}).data
        self.data.update({'first_name': 'Changed'})

    def test_can_update_user(self):
        response = self.client.put(reverse('student-detail', args=[self.student.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteUserTest(APITestCase):
    def setUp(self):
        self.instructor_credentials, instructor = testdata.create_instructor(user_data)
        self.student_credentials, student = testdata.create_student(testdata.user_data)
        self.client.force_login(self.instructor_credentials)

    def test_can_delete_student(self):
        response = self.client.delete(reverse('student-detail', args=[self.student_credentials.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_delete_instructor(self):
        response = self.client.delete(reverse('instructor-detail', args=[self.instructor_credentials.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)