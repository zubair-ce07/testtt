from __future__ import unicode_literals
from django.contrib import admin
from .models import User, Student, Tutor, Feedback, Invite

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Invite)
admin.site.register(Feedback)
