from django.contrib import admin


from .models import Employee
# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')


admin.site.register(Employee, EmployeeAdmin)
