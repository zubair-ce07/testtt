from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_teacher = False
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    object = CustomUserManager()
    def __str__(self):
        return self.email

class Quiz(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    class meta:
        verbose_name_plural: 'Quizzes'

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)


    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text

class TakenQuiz(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class meta:
        verbose_name_plural: 'TakenQuizzes'


class SelectedOption(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='Attempted')
    Answer =  models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='Choosed')

