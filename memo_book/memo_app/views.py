from django.shortcuts import render
from django.views import  View
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignupForm, LoginForm, AddMemoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Memory


class Home(View):
    def get(self, request):
        page = loader.get_template('memo_app/home.html')
        memories_of_user = Memory.objects.filter(user_id_id = request.session.__getitem__('user_id'))
        paginator = Paginator(memories_of_user, 5)
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
        page = loader.get_template('memo_app/login_signup.html')
        signup_from = SignupForm()
        login_form = LoginForm()
        context = {'signup_form': signup_from, 'login_form': login_form}
        return HttpResponse(page.render(context, request))


    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_data = login_form.cleaned_data;
            user = User.objects.filter(email=login_data['email'], password=login_data['password']).first()
            if user is not None:
                request.session.__setitem__('user_name', user.name)
                request.session.__setitem__('user_id', user.id)
                return HttpResponseRedirect('/home')
            else:
                page = loader.get_template('memo_app/login_signup.html')
                signup_from = SignupForm()
                context = {'signup_form': signup_from, 'login_form': login_form,
                           'is_sign_up': False, 'error_message': 'Email or password is not correct'}
                return HttpResponse(page.render(context, request))
        else:
            page = loader.get_template('memo_app/login_signup.html')
            signup_from = SignupForm()
            context = {'signup_form': signup_from, 'login_form': login_form, 'is_sign_up': False}
            return HttpResponse(page.render(context, request))


class SignUp(View):
    def get(self, request):
        page = loader.get_template('memo_app/login_signup.html')
        signup_from = SignupForm()
        login_form = LoginForm()
        context = {'signup_form': signup_from, 'login_form': login_form, 'is_sign_up': True}
        return HttpResponse(page.render(context, request))

    def post(self, request):
        new_user = User()
        signup_from = SignupForm(request.POST)
        if signup_from.is_valid():
            user_data = signup_from.cleaned_data
            new_user.name = user_data['name']
            new_user.email = user_data['email']
            new_user.password = user_data['password']
            new_user.user_name = user_data['username']
            new_user.save()
            request.session.__setitem__('user_name', new_user.name)
            request.session.__setitem__('user_id', new_user.id)
            return HttpResponseRedirect('/home')
        else:
            login_form = LoginForm()
            page = loader.get_template('memo_app/login_signup.html')
            context = {'signup_form': signup_from, 'login_form': login_form, 'is_sign_up': True}
            return HttpResponse(page.render(context, request))


class Logout(View):
    def post(self, request):
        request.session.clear()
        return HttpResponseRedirect('/')


class AddMemo(View):
    def post(self, request):
        memo_form = AddMemoForm(request.POST)
        if memo_form.is_valid():
            memo_data = memo_form.cleaned_data
            memo = Memory()
            memo.title = memo_data['title']
            memo.url = memo_data['url']
            memo.text = memo_data['memo_text']
            memo.tags = memo_data['tags']
            memo.user_id_id = request.session.__getitem__('user_id')
            memo.save()
            return HttpResponseRedirect('/home')
        else:
            page = loader.get_template('memo_app/home.html')
            context = {'memo_form': memo_form}
            return HttpResponse(page.render(context, request))


class DeleteMemo(View):
    def post(self, request):
         id = request.POST.get('memo_id')
         memory = Memory.objects.get(pk=id)
         memory.delete()
         return HttpResponseRedirect('/home')


class EditMemo(View):
    def get(self, request):
        id = request.GET.get('memo_id')
        memory = Memory.objects.get(pk=id)
        memo_form = AddMemoForm(initial={'title': memory.title, 'memo_text': memory.text,
                                         'url': memory.url, 'tags': memory.tags})
        page = loader.get_template('memo_app/edit_memo.html')
        context = {'memo_form': memo_form, 'memo_id': id}
        return HttpResponse(page.render(context, request))

    def post(self,request):
        memo_form = AddMemoForm(request.POST)
        id = request.POST.get('memo_id')
        if memo_form.is_valid():
            memo_data = memo_form.cleaned_data
            memo = Memory.objects.get(pk=id)
            memo.title = memo_data['title']
            memo.url = memo_data['url']
            memo.text = memo_data['memo_text']
            memo.tags = memo_data['tags']
            memo.save()
            return HttpResponseRedirect('/home')
        else:
            page = loader.get_template('memo_app/edit_memo.html')
            context = {'memo_form': memo_form, 'memo_id': id}
            return HttpResponse(page.render(context, request))



