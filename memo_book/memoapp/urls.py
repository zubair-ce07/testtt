from django.conf.urls import url
from django.conf.urls.static import static
from memo_book import settings
from .views import Login, SignUp, Home, Logout, AddMemo, AddCategory,\
    DeleteMemo, EditMemo, UserProfile, EditProfile, Search, Public, Logs


app_name = 'memoapp'
urlpatterns = [
    url(r'^$', Login.as_view(), name='loginsignup'),
    url(r'^signup$', SignUp.as_view()),
    url(r'^login$', Login.as_view()),
    url(r'^logout$', Logout.as_view()),
    url(r'^home$', Home.as_view(), name='home'),
    url(r'^addmemo$', AddMemo.as_view()),
    url(r'^deletememo$', DeleteMemo.as_view()),
    url(r'^editmemo$', EditMemo.as_view()),
    url(r'^profile$', UserProfile.as_view()),
    url(r'^editprofile$', EditProfile.as_view()),
    url(r'^search$', Search.as_view()),
    url(r'^public$', Public.as_view()),
    url(r'^activities$', Logs.as_view()),
    url(r'^addcategory', AddCategory.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
