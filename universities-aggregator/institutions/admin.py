from django.contrib import admin

# Register your models here.
from institutions.models import Institution, Program, Campus, Semester, Course

admin.site.register(Institution)
admin.site.register(Campus)
admin.site.register(Program)
admin.site.register(Semester)
admin.site.register(Course)
