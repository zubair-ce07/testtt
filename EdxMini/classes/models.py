from django.core.validators import URLValidator
from django.db import models

CHOICES = (
    ('Passed', 'Passed'),
    ('Failed', 'Failed'),
    ('Dropped', 'Dropped'),
    ('Active', 'Active')
)


class Student(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    father_name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='Student/', blank=True, null=True)
    registration_num = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return '{} {}'.format(self.first_name, self.last_name)


class Instructor(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    contact = models.CharField(max_length=64)
    qualification = models.CharField(max_length=256)
    image = models.ImageField(upload_to='Instructor/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return '{} {}'.format(self.first_name, self.last_name)


class Course(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=32)
    dept = models.CharField(max_length=64)
    image = models.ImageField(upload_to='Course/', blank=True, null=True)
    intro_video = models.URLField(validators=[URLValidator()], blank=True)
    instructors = models.ManyToManyField(Instructor)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    status = models.CharField(max_length=32, choices=CHOICES, default='Active')
    joining_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
