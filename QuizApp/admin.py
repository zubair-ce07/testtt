from django.contrib import admin

from QuizApp.models import *

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['email',]

admin.site.register(CustomUser)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TakenQuiz)
admin.site.register(SelectedOption)