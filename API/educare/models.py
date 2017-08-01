from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import CustomUserManager
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    LOCATION_CHOICES = (
        ('LHR', 'Lahore'),
        ('FSD', 'Faisalabad'),
        ('KHI', 'Karachi'),
        ('ISL', 'Islamabad'),
        ('PEW', 'Peshawar'),
        ('MUL', 'Multan'),
    )

    SUBJECTS_CHOICES = (
        ('Math', 'Mathematics'),
        ('Eng', 'English'),
        ('Bio', 'Biology'),
        ('Chem', 'Chemistry'),
        ('Phy', 'Physics'),
        ('Acc', 'Accounting'),
        ('BStd', 'Business Studies'),
        ('Eco', 'Economics'),
    )

    USER_TYPE_CHOICES = (
        ('T', 'Tutor'),
        ('S', 'Student'),
    )

    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(default=date.today)
    biography = models.TextField(max_length=200, null=True)
    profile_picture = models.ImageField(upload_to='img_folder/', default='img_folder/default.jpeg')
    location = models.CharField(choices=LOCATION_CHOICES, max_length=3)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=1)
    subjects = ArrayField(models.CharField(choices=SUBJECTS_CHOICES, max_length=4, default=''), default=[], size=8)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'gender', 'location', 'subjects']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        managed = True

    def get_full_name(self):
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()


class Tutor(User):
    education = models.TextField(max_length=200, null=False)
    phone_number = PhoneNumberField(default='+92')
    objects = CustomUserManager()


class Student(User):

    GRADE_CHOICES = (
        ('PreNur', 'Pre-Nursery'),
        ('Nur', 'Nursery'),
        ('KG', 'Kindergarten'),
        ('GR-1', 'Grade 1'),
        ('GR-2', 'Grade 2'),
        ('GR-3', 'Grade 3'),
        ('GR-4', 'Grade 4'),
        ('GR-5', 'Grade 5'),
        ('GR-6', 'Grade 6'),
        ('GR-7', 'Grade 7'),
        ('GR-8', 'Grade 8'),
        ('MAT-9', 'Matric Grade 9'),
        ('MAT-10', 'Matric Grade 10'),
        ('OL-9', 'Olevels Grade 9'),
        ('OL-10', 'Olevels Grade 10'),
        ('OL-11', 'Olevels Grade 11'),
    )

    grade = models.CharField(choices=GRADE_CHOICES, max_length=10)
    objects = CustomUserManager()


class Feedback(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0)

    def __unicode__(self):
        return 'Text: %s  Rating: %f Given by %s' % (self.text, self.rating, self.student.get_full_name())


class Invite(models.Model):
    accepted = models.BooleanField(default=False)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField(max_length=200)
    accepting_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s Sent by %s' % (self.message, self.tutor.get_full_name())


@receiver(post_save, sender=Student)
@receiver(post_save, sender=Tutor)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
