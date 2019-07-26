from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.models import ModelForm

from QuizApp.models import Answer, CustomUser, Question, Quiz


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email','is_teacher', 'is_student')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email',)

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
