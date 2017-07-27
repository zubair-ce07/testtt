from django.contrib import admin

# Register your models here.
from .models import WeatherModel


class WeatherAdmin(admin.ModelAdmin):
    list_display = ('id', 'max_temp', 'min_temp', 'max_dew', 'min_dew',
                    'max_humidity', 'min_humidity', 'max_sea_pressure',
                    'min_sea_pressure', 'max_visibility', 'min_visibility',)


admin.site.register(WeatherModel, WeatherAdmin)
