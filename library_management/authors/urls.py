from django.urls import path

from . import views

app_name = 'authors'
urlpatterns = [
    path('authors/', views.AuthorList.as_view(), name='authors-index'),
    path('authors_data_list/', views.AuthorDataList.as_view(),
         name='authors-data-index'),
    path('author/<int:pk>/',
         views.AuthorDetail.as_view(),
         name='author-detail'),
    path('author/<int:pk>/delete',
         views.AuthorDestroy.as_view(),
         name='author-delete'),
    path('author/<int:pk>/update',
         views.AuthorUpdate.as_view(),
         name='author-update'),
    path('author/<int:pk>/books/',
         views.AuthorBooksList.as_view(),
         name='author-books'),
]
