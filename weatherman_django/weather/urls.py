"""
this module contains the urls of this django app
"""
from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('yearly/<str:year>', views.YearlyTemperature.as_view(), name="yearly_temperature"),
    path('average-monthly/<str:year>', views.AverageTemperature.as_view(),
         name="average_monthly"),
    path('average-monthly/<str:year>/<str:month>', views.AverageTemperature.as_view(),
         name="average_monthly"),
    path('cities/', views.GetAllCities.as_view(), name="get_cities"),
    path('years/<int:city>', views.GetYearsOfCity.as_view(), name="get_years"),
]
