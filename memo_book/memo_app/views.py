from django.shortcuts import render
from django.views import  View
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignupForm, LoginForm, AddMemoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Memory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(LoginRequiredMixin, View):
    def get(self, request):
        page = loader.get_template('memo_app/home.html')
        memories_of_user = Memory.objects.filter(user_id_id = request.user.id)
        paginator = Paginator(memories_of_user, 2)
        page_no = request.GET.get('page_no')
        try:
            memos = paginator.page(page_no)
        except PageNotAnInteger:
            memos = paginator.page(1)
        except EmptyPage:
            memos = paginator.page(paginator.num_pages)

        context = {'memo_form': AddMemoForm(), 'memories_of_user': memos}
        return HttpResponse(page.render(context, request))


class Login(View):
    def get(self, request):
        if not request.user.is_authenticated():
            page = loader.get_template('memo_app/login_signup.html')
            signup_from = SignupForm()
            login_form = LoginForm()
            context = {'signup_form': signup_from, 'login_form': login_form}
            return HttpResponse(page.render(context, request))
        else:
            return HttpResponseRedirect('/home')


    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_data = login_form.cleaned_data
            username = login_data['username']
            password = login_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                page = loader.get_template('memo_app/login_signup.html')
                signup_from = SignupForm()
                context = {'signup_form': signup_from, 'login_form': login_form,
                           'is_sign_up': False, 'error_message': 'Username or password is not correct'}
                return HttpResponse(page.render(context, request))
        else:
            page = loader.get_template('memo_app/login_signup.html')
            signup_from = SignupForm()
            context = {'signup_form': signup_from, 'login_form': login_form, 'is_sign_up': False}
            return HttpResponse(page.render(context, request))


class SignUp(View):
    def get(self, request):
        if not request.user.is_authenticated():
            page = loader.get_template('memo_app/login_signup.html')
            signup_from = SignupForm()
            login_form = LoginForm()
            context = {'signup_form': signup_from, 'login_form': login_form, 'is_sign_up': True}
            return HttpResponse(page.render(context, request))
        else:
            return HttpResponseRedirect('/home')

    def post(self, request):
        signup_from = SignupForm(request.POST)
        if signup_from.is_valid():
            user_data = signup_from.cleaned_data
            try:
                new_user = User.objects.create_user(user_data['username'], user_data['email'],  user_data['password'])
                new_user.first_name = user_data['first_name']
                new_user.last_name = user_data['last_name']
                new_user.save()
                login(request, new_user)
                return HttpResponseRedirect('/home')
            except:
                login_form = LoginForm()
                page = loader.get_template('memo_app/login_signup.html')
                context = {'signup_form': signup_from, 'login_form': login_form,'username_error':
                           'User Name Already exists ', 'is_sign_up': True}
                return HttpResponse(page.render(context, request))
        else:
            login_form = LoginForm()
            page = loader.get_template('memo_app/login_signup.html')
            context = {'signup_form': signup_from, 'login_form': login_form, 'is_sign_up': True}
            return HttpResponse(page.render(context, request))


class Logout(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class AddMemo(LoginRequiredMixin, View):
    def post(self, request):
        memo_form = AddMemoForm(request.POST,  request.FILES)
        if memo_form.is_valid():
            memo_data = memo_form.cleaned_data
            memo = Memory()
            memo.title = memo_data['title']
            memo.url = memo_data['url']
            memo.text = memo_data['memo_text']
            memo.tags = memo_data['tags']
            memo.user_id_id = request.user.id
            memo.image = '/images/'
            memo.save()
            image = request.FILES['image']
            image.name = str(memo.id)+'.jpg'
            save_images(image)
            memo.image = str(memo.image) + image.name
            memo.save()
            return HttpResponseRedirect('/home')
        else:
            page = loader.get_template('memo_app/home.html')
            context = {'memo_form': memo_form}
            return HttpResponse(page.render(context, request))


class DeleteMemo(LoginRequiredMixin, View):
    def post(self, request):
         id = request.POST.get('memo_id')
         memory = Memory.objects.get(pk=id)
         memory.delete()
         return HttpResponseRedirect('/home')


class EditMemo(LoginRequiredMixin,View):
    def get(self, request):
        id = request.GET.get('memo_id')
        memory = Memory.objects.get(pk=id)
        memo_form = AddMemoForm(initial={'title': memory.title, 'memo_text': memory.text,
                                         'url': memory.url, 'tags': memory.tags})
        page = loader.get_template('memo_app/edit_memo.html')
        context = {'memo_form': memo_form, 'memo_id': id}
        return HttpResponse(page.render(context, request))

    def post(self,request):
        memo_form = AddMemoForm(request.POST, request.FILES)
        id = request.POST.get('memo_id')
        if memo_form.is_valid():
            memo_data = memo_form.cleaned_data
            memo = Memory.objects.get(pk=id)
            memo.title = memo_data['title']
            memo.url = memo_data['url']
            memo.text = memo_data['memo_text']
            memo.tags = memo_data['tags']
            image = request.FILES['image']
            image.name = str(memo.id) + '.jpg'
            save_images(image)
            memo.save()
            return HttpResponseRedirect('/home')
        else:
            page = loader.get_template('memo_app/edit_memo.html')
            context = {'memo_form': memo_form, 'memo_id': id}
            return HttpResponse(page.render(context, request))


class UserProfile(LoginRequiredMixin, View):
    def get(self,request):
        page = loader.get_template('memo_app/profile.html')
        context = {}
        return HttpResponse(page.render(context, request))


class EditProfile(LoginRequiredMixin, View):

    def get(self, request):
        page = loader.get_template('memo_app/edit_profile.html')
        user_form = SignupForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name,
                                        'username': request.user.username, 'email': request.user.email,
                                        'password':'temporary to handle not valid'})
        user_form.fields['password'].widget.attrs['class'] = 'hidden'
        context = {'user_form': user_form}
        return HttpResponse(page.render(context, request))

    def post(self, request):
        user_form = SignupForm(request.POST)
        user_form.fields['password'].widget.attrs['class'] = 'hidden'
        if user_form.is_valid():
            user_data = user_form.cleaned_data
            user = User.objects.get(pk=request.user.id)
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.username = user_data['username']
            user.email = user_data['email']
            user.save()
            return HttpResponseRedirect('/home')
        else:
            page = loader.get_template('memo_app/edit_profile.html')
            context = {'user_form': user_form}
            return HttpResponse(page.render(context, request))



# Global method to save image files
def save_images(image):
        with open('memo_app/static/images/' + image.name, 'wb+') as destination:
            for img in image.chunks():
                destination.write(img)