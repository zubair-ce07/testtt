from django.contrib import admin
from AppraisalApp import models
# Register your models here.


admin.site.register(models.Employee)
admin.site.register(models.Competency)
admin.site.register(models.Feedback)

