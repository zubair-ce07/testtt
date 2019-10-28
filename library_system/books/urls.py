from django.urls import path
from books import views


urlpatterns = [
    path('book-home', views.BooksListView.as_view(), name='book-home'),
    path('book/<int:pk>/', views.BooksDetailView.as_view(), name='book_detail'),
    path('book/new/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    path('book/<int:pk>/issue/', views.BookIssue, name='book_issue'),
    path('book/<int:pk>/user_information/', views.user_profile, name='user_profile'),
    path('book/<int:pk>/request/', views.BookRequest, name='book_request'),
    path('book/<int:pk>/user_books/', views.IssueBookListView.as_view(), name='user_books'),
    path('book/<int:pk>/user_requests/', views.UserRequestsListView.as_view(), name='user_requests'),
    path('book/user_books/', views.BorrowListView.as_view(), name='borrow_books'),
    path('book/<int:pk>/issuebook_delete/', views.IssuebookDeleteView.as_view(), name='isuebook_delete'),
    path('book/<int:pk>/request_delete/', views.RequestbookDeleteView.as_view(), name='requests_delete'),
    path('book/1/user_books/', views.MyView.as_view(), name='direct'),
    path('book/1/user_requests/', views.RequestView.as_view(), name='direct_requests'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>/view_info', views.view_info, name='view_info'),
]
