from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# router.register(r'', views.PayslipLineViewset, base_name='users')
router.register(r'', views.EmployeesPayrollViewset, base_name='users')

urlpatterns = router.urls
