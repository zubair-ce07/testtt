from django.urls import path
from . import views

app_name = 'appraisal'

urlpatterns = [
    path('signup/', views.signup_user, name='signup'),
    path('home/', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('employees/', views.EmployeeView.as_view(), name='employees'),
    path('employee_detail/<int:uid>', views.employee_detail, name='employee_detail'),
    path('send_feedback/<int:uid>', views.send_feedback, name='send_feedback'),

]
