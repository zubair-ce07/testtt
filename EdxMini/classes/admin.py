from django.contrib import admin
from  classes.models import Student, Instructor, Course, Enrollment


admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(Course)
admin.site.register(Instructor)
