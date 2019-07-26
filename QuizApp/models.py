from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, unique=True)
    objects = UserManager()

    def __str__(self):
        return self.email


class Quiz(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
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

    class Meta:
        verbose_name_plural: 'TakenQuizzes'

    def __str__(self):
        return self.student.email


class SelectedOption(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='Attempted')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='Choosed')

    def __str__(self):
        return self.answer.text
