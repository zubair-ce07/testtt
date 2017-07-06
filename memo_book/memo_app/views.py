from django.shortcuts import render
from django.views import  View
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from memo_app.forms import SignupForm, LoginForm, AddMemoForm, EditProfileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from memo_app.models import User, Memory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password


class Home(LoginRequiredMixin, View):
    def get(self, request):
        page = loader.get_template('memo_app/home.html')
        memories_of_user = Memory.objects.filter(user_id = request.user.id)
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
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.save(commit=False)
            signup_form.password = make_password(signup_form.cleaned_data['password'])
            signup_form.save()
            login(request, signup_form.instance)
            return HttpResponseRedirect('/home')
        else:
            login_form = LoginForm()
            page = loader.get_template('memo_app/login_signup.html')
            context = {'signup_form': signup_form, 'login_form': login_form, 'is_sign_up': True}
            return HttpResponse(page.render(context, request))


class Logout(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class AddMemo(LoginRequiredMixin, View):
    def post(self, request):
        memo_form = AddMemoForm(request.POST,  request.FILES)
        if memo_form.is_valid():
            memo = memo_form.save(commit=False)
            memo.user_id = request.user.id
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
         memory.image.delete(False)
         memory.delete()
         return HttpResponseRedirect('/home')


class EditMemo(LoginRequiredMixin,View):
    def get(self, request):
        id = request.GET.get('memo_id')
        memory = Memory.objects.get(pk=id)
        memo_form = AddMemoForm(instance=memory)
        page = loader.get_template('memo_app/edit_memo.html')
        context = {'memo_form': memo_form, 'memo_id': id}
        return HttpResponse(page.render(context, request))

    def post(self,request):
        id = request.POST.get('memo_id')
        memory = Memory.objects.get(pk=id)
        memory.image.delete(False)
        memo_form = AddMemoForm(request.POST, request.FILES,instance=memory)
        if memo_form.is_valid():
            memo_form.save()
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
        user_form = EditProfileForm(instance=request.user)
        context = {'user_form': user_form}
        return HttpResponse(page.render(context, request))

    def post(self, request):
        user_form = EditProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect('/home')
        else:
            page = loader.get_template('memo_app/edit_profile.html')
            context = {'user_form': user_form}
            return HttpResponse(page.render(context, request))
