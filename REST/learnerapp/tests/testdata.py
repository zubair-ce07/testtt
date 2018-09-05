import datetime

from learnerapp import models

post_course = {'title': 'Django tests', 'subject': 'CS', 'organization': 'FAST', 'description': 'check tests',
               'start_date': datetime.date(2018, 10, 1), 'end_date': datetime.date(2018, 11, 1), 'status': 'active',
               'level': 'beginner'}
post_student = {'user': {'username': 'zainab_student', 'password': '1234asdf', 'first_name': 'Zainab',
                         'last_name': 'Amir', 'email': 'zainab.amir@arbisoft.com'}, 'university': 'FAST-NU',
                'dob': datetime.date(1995, 9, 10)}
post_instructor = {'user': {'username': 'zainab', 'password': '1234asdf', 'first_name': 'Zainab',
                            'last_name': 'Amir', 'email': 'zainab.amir@arbisoft.com'}, 'institute': 'FAST-NU'}

user_data = {'username': 'zainabamir', 'first_name': 'Zainab', 'last_name': 'Amir', 'email': 'zainab.amir@arbisoft.com'}
student_data = {'dob': datetime.date(1995, 9, 10), 'university': 'FAST-NU'}
instructor_data = {'institute': 'FAST-NU', 'designation': 'Lab Teacher'}


def create_user(data):
    user = models.CustomUser.objects.create(**data)
    user.set_password('1234asdf')
    user.save()
    return user


def create_instructor(user_info):
    user = create_user(user_info)
    instructor = models.Instructor.objects.create(user=user, **instructor_data)
    return user, instructor


def create_student(user_info):
    user_info['user_type'] = 1
    user = create_user(user_info)
    student = models.Student.objects.create(user=user, **student_data)
    return user, student