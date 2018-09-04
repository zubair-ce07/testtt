import datetime

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from learnerapp import models

user_data = {'username': 'zainab', 'first_name': 'Zainab', 'user_type': 1,
             'last_name': 'Amir', 'email': 'zainab.amir@arbisoft.com'}
student_data = {'dob': datetime.date(1995, 9, 10), 'university': 'FAST-NU'}


def create_user(user_data):
    user = models.CustomUser.objects.create(**user_data)
    user.set_password('1234asdf')
    user.save()
    return user


def create_student(user_info):
    user = create_user(user_info)
    student = models.Student.objects.create(user=user, **student_data)
    return user, student


class CreateUserTest(APITestCase):
    def setUp(self):
        self.superuser = models.CustomUser.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.student = {'user':
                       {'username': 'zainab_student', 'password': '1234asdf', 'first_name': 'Zainab',
                        'last_name': 'Amir', 'email': 'zainab.amir@arbisoft.com'},
                        'university': 'FAST-NU', 'dob': datetime.date(1995, 9, 10)}

        self.instructor = {'user':
                          {'username': 'zainab', 'password': '1234asdf', 'first_name': 'Zainab',
                           'last_name': 'Amir', 'email': 'zainab.amir@arbisoft.com'}, 'institute': 'FAST-NU'}

    def test_can_create_instructor(self):
        response = self.client.post(reverse('instructor-list'), self.instructor)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_student(self):
        response = self.client.post(reverse('student-list'), self.student)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CreateCourseTest(APITestCase):
    def setUp(self):
        self.superuser = models.CustomUser.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.course = {'title': 'Django tests', 'subject': 'CS', 'organization': 'FAST',
                       'description': 'check tests', 'start_date': datetime.date(2018, 10, 1),
                       'end_date': datetime.date(2018, 11, 1), 'status': 'active', 'level': 'beginner'}

    def test_can_create_course(self):
        response = self.client.post(reverse('course-list'), self.course)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StudentReadTest(APITestCase):
    def setUp(self):
        user, self.student = create_student(user_data)
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