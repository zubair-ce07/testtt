from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    BlogList,
    BlogDetail,
    TagList,
    TagDetail,
    CommentList,
    CommentDetail
)

urlpatterns = [
    path('tags/<int:pk>', TagDetail.as_view()),
    path('tags/', TagList.as_view()),
    path('<int:pk>', BlogDetail.as_view()),
    path('', BlogList.as_view()),
    path('comments/<int:pk>', CommentDetail.as_view()),
    path('comments/', CommentList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
