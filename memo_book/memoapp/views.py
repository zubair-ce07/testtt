from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.db.models import Q

from memoapp.forms import SignupForm, LoginForm, AddMemoForm, EditProfileForm, Category
from memoapp.models import User, Memory
from memoapp.signals import user_login, user_logout
from memoapp.receivers import receiver


class Home(LoginRequiredMixin, View):
    def get(self, request):
        memories_of_user = request.user.memory_set.all()
        paginator = Paginator(memories_of_user, 2)
        page_no = request.GET.get('page_no')
        try:
            memos = paginator.page(page_no)
        except PageNotAnInteger:
            memos = paginator.page(1)
        except EmptyPage:
            memos = paginator.page(paginator.num_pages)

        memo_form = AddMemoForm()
        memo_form.fields['category'].queryset = request.user.category_set.all()
        context = {'memo_form': memo_form, 'memos': memos}
        return render(request, 'memoapp/home.html', context)


class Login(View):
    def get(self, request):
        if not request.user.is_authenticated():
            signup_from = SignupForm()
            login_form = LoginForm()
            context = {'signup_form': signup_from, 'login_form': login_form}
            return render(request, 'memoapp/login_signup.html', context)
        else:
            return HttpResponseRedirect(reverse('memoapp:home'))

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_data = login_form.cleaned_data
            email = login_data['email']
            password = login_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                print('asdkfjashdkjf')
                print(user.is_authenticated())
                request.user = user
                user_login.send(sender=None, user_name=user.username)
                return HttpResponseRedirect(reverse('memoapp:home'))
            else:
                signup_from = SignupForm()
                context = {'signup_form': signup_from, 'login_form': login_form,
                           'view': 'login', 'error_message': 'Username or password is not correct'}
                return render(request, 'memoapp/login_signup.html', context)
        else:
            signup_from = SignupForm()
            context = {'signup_form': signup_from, 'login_form': login_form, 'view': 'login'}
            return render(request, 'memoapp/login_signup.html', context)


class SignUp(View):
    def get(self, request):
        if not request.user.is_authenticated():
            signup_from = SignupForm()
            login_form = LoginForm()
            context = {'signup_form': signup_from, 'login_form': login_form, 'view': 'signup'}
            return render(request, 'memoapp/login_signup.html', context)
        else:
            return HttpResponseRedirect(reverse('memoapp:home'))

    def post(self, request):
        signup_form = SignupForm(request.POST, request.FILES)
        if signup_form.is_valid():
            new_user = signup_form.save(commit=False)
            new_user.password = make_password(signup_form.cleaned_data['password'])
            new_user.save()
            login(request, signup_form.instance)
            return HttpResponseRedirect(reverse('memoapp:home'))
        else:
            login_form = LoginForm()
            context = {'signup_form': signup_form, 'login_form': login_form, 'view': 'signup'}
            return render(request, 'memoapp/login_signup.html', context)


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user.username
        logout(request)
        user_logout.send(sender=None, user_name=username)
        return HttpResponseRedirect(reverse('memoapp:loginsignup'))


class AddMemo(LoginRequiredMixin, View):
    def post(self, request):
        memo_form = AddMemoForm(request.POST,  request.FILES)
        memo_form.fields['category'].queryset = request.user.category_set.all()
        if memo_form.is_valid():
            memo = memo_form.save(commit=False)
            memo.user_id = request.user.id
            memo.save()
            return HttpResponseRedirect(reverse('memoapp:home'))
        else:
            context = {'memo_form': memo_form}
            return render(request, 'memoapp/home.html', context)


class DeleteMemo(LoginRequiredMixin, View):
    def post(self, request):
         id = request.POST.get('memo_id')
         memory = Memory.objects.get(pk=id)
         memory.image.delete(False)
         memory.delete()
         return HttpResponseRedirect(reverse('memoapp:home'))


class EditMemo(LoginRequiredMixin,View):
    def get(self, request):
        id = request.GET.get('memo_id')
        memory = Memory.objects.get(pk=id)
        memo_form = AddMemoForm(instance=memory)
        memo_form.fields['category'].queryset = request.user.category_set.all()
        print (memo_form.instance.image)
        memo_form.fields['category'].queryset = request.user.category_set.all()

        context = {'memo_form': memo_form, 'memo_id': id}
        return render(request, 'memoapp/edit_memo.html', context)

    def post(self,request):
        id = request.POST.get('memo_id')
        memory = Memory.objects.get(pk=id)

        memo_form = AddMemoForm(request.POST, request.FILES,instance=memory)
        memo_form.fields['category'].queryset = request.user.category_set.all()
        if memo_form.is_valid():
            print('*****')
            print(memo_form.instance.image)
            memo_form.save()
            return HttpResponseRedirect(reverse('memoapp:home'))
        else:
            context = {'memo_form': memo_form, 'memo_id': id}
            return render(request, 'memoapp/edit_memo.html', context)


class UserProfile(LoginRequiredMixin, View):
    def get(self,request):
        return render(request, 'memoapp/profile.html')


class EditProfile(LoginRequiredMixin, View):
    def get(self, request):
        user_form = EditProfileForm(instance=request.user)
        context = {'user_form': user_form}
        return render(request, 'memoapp/edit_profile.html', context)

    def post(self, request):
        user_form = EditProfileForm(request.POST,request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('memoapp:home'))
        else:
            context = {'user_form': user_form}
            return render(request, 'memoapp/edit_profile.html', context)


class Search(LoginRequiredMixin, View):
    def post(self, request):
        search_text = request.POST['tosearch']
        searched_mems = request.user.memory_set.filter(Q(title__icontains=search_text) |
                                                       Q(tags__icontains=search_text) |
                                                       Q(text__icontains=search_text))
        paginator = Paginator(searched_mems, 2)
        page_no = request.GET.get('page_no')
        try:
            memos = paginator.page(page_no)
        except PageNotAnInteger:
            memos = paginator.page(1)
        except EmptyPage:
            memos = paginator.page(paginator.num_pages)
        memo_form = AddMemoForm()
        memo_form.fields['category'].queryset = request.user.category_set.all()
        context = {'memo_form': memo_form, 'memos': memos, 'text': search_text}
        return render(request, 'memoapp/home.html', context)

    def get(self, request):
        search_text = request.GET['tosearch']
        searched_mems = request.user.memory_set.filter(Q(title__icontains=search_text) |
                                                       Q(tags__icontains=search_text) |
                                                       Q(text__icontains=search_text))
        paginator = Paginator(searched_mems, 2)
        page_no = request.GET.get('page_no')
        try:
            memos = paginator.page(page_no)
        except PageNotAnInteger:
            memos = paginator.page(1)
        except EmptyPage:
            memos = paginator.page(paginator.num_pages)
        memo_form = AddMemoForm()
        memo_form.fields['category'].queryset = request.user.category_set.all()
        context = {'memo_form': memo_form, 'memos': memos, 'text': search_text}
        return render(request, 'memoapp/home.html', context)


class Public(LoginRequiredMixin, View):
        def get(self, request):
            public_mems = Memory.public_memories.all()
            paginator = Paginator(public_mems, 5)
            page_no = request.GET.get('page_no')
            try:
                memos = paginator.page(page_no)
            except PageNotAnInteger:
                memos = paginator.page(1)
            except EmptyPage:
                memos = paginator.page(paginator.num_pages)

            context = {'public_mems': memos}
            return render(request, 'memoapp/public.html', context)


class Logs(LoginRequiredMixin, View):
    def get(self, request):
        logs = request.user.activity_set.all()
        return render(request, 'memoapp/activities.html', {'logs': logs})


class AddCategory(LoginRequiredMixin, View):
    def get(self, request):
        category_form = Category()
        return render(request, 'memoapp/addcategory.html', {'category_form': category_form})

    def post(self, request):
        category_form = Category(request.POST)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.user_id = request.user.id
            category.save()
            return HttpResponseRedirect(reverse('memoapp:home'))
        else:
            return render(request, 'memoapp/addcategory.html', {'category_form': category_form})
