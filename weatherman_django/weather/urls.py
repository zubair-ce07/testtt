from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('yearly/<str:year>', views.YearlyTemperature.as_view(), name="yearly_temperature"),
    path('average-monthly/<str:year>/<str:month>', views.AverageTemperature.as_view(),
         name="average_monthly"),
]
