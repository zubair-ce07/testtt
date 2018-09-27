from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView

from system.views import loginUser, signupUser, logoutUser, \
    change_password, AppraisalDeleteView, AppraisalView, \
    EmployeeListView, AppraisalListView, index

urlpatterns = [
    path('', index, name='home'),
    path('login', loginUser, name='login'),
    path('signup', signupUser, name='signup'),
    path('logout', login_required(logoutUser), name='logout'),
    path('password', change_password, name='change_password'),

    path('admin', RedirectView.as_view(url='/admin'), name='admin_home'),
    path('employees', EmployeeListView.as_view(), name='view_employees'),

    path('appraisal/view/<int:pk>', AppraisalListView.as_view(),
         name='view_appraisals'),
    path('appraisal/add', AppraisalView.as_view(), name='add_appraisal'),
    path('apparaisal/delete/<int:id>', AppraisalDeleteView.as_view(),
         name='delete_appraisal'),
    path('apparaisal/update/<int:id>', AppraisalView.as_view(),
         name='update_appraisal'),
]
