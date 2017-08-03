from rest_framework.routers import DefaultRouter
from backend.categories.views.category import CategoryViewSet

app_name = 'category'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls
