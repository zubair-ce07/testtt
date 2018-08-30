from learnerapp import models

from django.contrib import admin

admin.site.register(models.CustomUser)
admin.site.register(models.Instructor)
admin.site.register(models.Course)
admin.site.register(models.Student)