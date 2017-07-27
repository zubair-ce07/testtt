from __future__ import unicode_literals
from django.contrib import admin
from .models import User, Student, Tutor

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Tutor)

