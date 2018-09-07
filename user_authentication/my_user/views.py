from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, \
    PasswordChangeForm
from .forms import UserEditForm


class IndexView(View):
    template_name = 'user/index.html'

    def get(self, request):
        return render(request, self.template_name)


class UserFormView(View):
    form_class = UserCreationForm
    template_name = 'user/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # Just for learning purposes, otherwise form.save() will save the data
            user = form.save(commit=False)
            # Just for learning purposes
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            # return User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('my_user:index')
            else:
                return

        return render(request, self.template_name, {'form': form})


class UserLoginFormView(View):
    form_class = AuthenticationForm
    template_name = 'user/login_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('my_user:index')
            else:
                error = "Please enter a valid username or password"
                return render(request, self.template_name, {'form': form, 'error_message': error})
        else:
            return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('my_user:index')


class UserEditFormView(View):
    form_class = UserEditForm

    template_name = 'user/edit_form.html'

    def get(self, request):
        form = self.form_class(instance=request.user, )
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # to save the current instance and not create a new instance
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_user:index')

        return render(request, self.template_name, {'form': form})


class UserEditPassword(View):
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'

    def get(self, request):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # to save the current instance and not create a new instance
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_user:index')

        return render(request, self.template_name, {'form': form})
