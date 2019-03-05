from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('home/', views.Home.as_view(), name="home"),
    path('edit_user/<int:pk>', views.EditUser.as_view(), name="edit_user"),

    path('add_contact/', views.AddContact.as_view(), name="add_contact"),
    path('edit_contact/<int:pk>', views.EditContact.as_view(), name="edit_contact"),
    path('delete_contact/<int:pk>', views.DeleteContact.as_view(), name="delete_contact"),
    path('contacts/', views.Contacts.as_view(), name="contacts"),

    path('add_todo/', views.AddTodo.as_view(), name="add_todo"),
    path('edit_todo/<int:pk>', views.EditTodo.as_view(), name="edit_todo"),
    path('delete_todo/<int:pk>', views.DeleteTodo.as_view(), name="delete_todo"),
    path('todos/', views.Todos.as_view(), name="todos"),

    path('add_item/<int:pk>', views.AddItem.as_view(), name="add_item"),
    path('edit_item/<int:todo_id>/<int:pk>', views.EditItem.as_view(), name="edit_item"),
    path('delete_item/<int:todo_id>/<int:pk>', views.DeleteItem.as_view(), name="delete_item"),
]
