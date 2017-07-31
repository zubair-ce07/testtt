from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient


from .models import Employee
# Create your tests here.


class EmployeeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.post('/employees/', {
            'username': 'osama',
            'first_name': 'Osama',
            'last_name': 'Arshad',
            'gender': 'M',
            'date_of_birth': '1996-2-2',
            'job_title': 'Software Engineer',
            'is_active': True,
            'date_of_joining': '2017-6-5',
            'nationality': 'Pakistani'
        })

    def test_user_fields_have_been_passed(self):
        """
        Test username, first_name and last_name one-to-one correspondance 
        with django User model
        """
        user = User.objects.get(username='osama')
        emp = Employee.objects.get(username='osama')

        self.assertEqual(emp.username, user.username)
        self.assertEqual(emp.first_name, user.first_name)
        self.assertEqual(emp.last_name, user.last_name)
    
    def test_reports_to_field_is_working(self):
        
