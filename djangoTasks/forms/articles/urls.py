from rest_framework.routers import SimpleRouter

from articles.views import *


router = SimpleRouter()
router.register(r'articles', ArticleViewSet)
urlpatterns = router.urls
