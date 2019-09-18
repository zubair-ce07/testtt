from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('post_reaction/', views.ReactionView.as_view(), name="post_reaction"),
    path('delete_favorite/', views.DeleteFavorite.as_view(), name="del_fav"),
]
