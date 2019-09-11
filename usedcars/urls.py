from django.urls import path
from . import views


app_name = 'usedcars'
urlpatterns = [
    # 127.0.0.1:8000/
    path('', views.index_view, name='index'),

    # /table/
    path('table', views.table_page, name='table'),

    # /[Make of company here]/
    path('<str:company_name>', views.detail_test, name='temp_view'),

    # /singleCar/23/
    path('singleCar/<int:car_id>', views.single_car, name='single_car_view')

]
