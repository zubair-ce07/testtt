from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'lms_api'
urlpatterns = [
    # Book routes
    path('books/', views.BookList.as_view(), name='books-index'),
    path('book/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('book/<int:pk>/delete',
         views.BookDestroy.as_view(),
         name='book-delete'),
    path('book/<int:pk>/update',
         views.BookUpdate.as_view(),
         name='book-update'),

    # Author routes
    path('authors/', views.AuthorList.as_view(), name='authors-index'),
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

    # Publisher routes
    path('publishers/', views.PublisherList.as_view(), name='authors-index'),
    path('publisher/<int:pk>/',
         views.PublisherDetail.as_view(),
         name='publisher-detail'),
    path('publisher/<int:pk>/delete',
         views.PublisherDestroy.as_view(),
         name='publisher-delete'),
    path('publisher/<int:pk>/update',
         views.PublisherUpdate.as_view(),
         name='publisher-update'),
    path('publisher/<int:pk>/books/',
         views.PublisherBooksList.as_view(),
         name='publisher-books'),

    # Category routes
    path('categories/', views.CategoryList.as_view(), name='categories-index'),
    path('category/', views.CategoryCreate.as_view(), name='category-create'),
    path('category/<int:pk>/',
         views.CategoryDetail.as_view(),
         name='category-detail'),
    path('category/<int:pk>/delete',
         views.CategoryDestroy.as_view(),
         name='category-delete'),
    path('category/<int:pk>/update',
         views.CategoryUpdate.as_view(),
         name='category-update'),

    # Auth routes
    path('accounts/signup/author/',
         views.AuthorSignup.as_view(),
         name='author_signup'),
    path('accounts/signup/publisher/',
         views.PubliserSignup.as_view(),
         name='publisher_signup'),
    path('login', obtain_auth_token, name='get_user_auth_token'),
    path('logout/', views.Logout.as_view(), name="log_out"),
]
