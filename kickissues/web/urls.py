from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from web.views import HomepageView

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('account/', include('web.account.urls')),
    path('issue/', include('web.issue.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
