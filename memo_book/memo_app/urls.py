from django.conf.urls import url
from .views import Login, SignUp, Home, Logout, AddMemo, DeleteMemo, EditMemo


app_name = 'memo_app'
urlpatterns = [
    url(r'^$', Login.as_view()),
    url(r'^signup$', SignUp.as_view()),
    url(r'^login$', Login.as_view()),
    url(r'^logout$', Logout.as_view()),
    url(r'^home$', Home.as_view()),
    url(r'^addmemo$', AddMemo.as_view()),
    url(r'^deletememo$', DeleteMemo.as_view()),
    url(r'^editmemo$', EditMemo.as_view())
]
