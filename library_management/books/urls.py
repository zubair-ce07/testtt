from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('books/', views.BookList.as_view(), name='books-index'),
    path('book/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('book/<int:pk>/delete',
         views.BookDestroy.as_view(),
         name='book-delete'),
    path('book/<int:pk>/update',
         views.BookUpdate.as_view(),
         name='book-update')
]
