"""
this module contains the views of this django app
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View, TemplateView
from .forms import UserRegisterForm, UserLoginForm, UserEditForm, UserChangePasswordForm


class IndexView(TemplateView):
    """
    this is TemplateView of Index page
    """
    template_name = 'user/index.html'


class UserFormView(View):
    """
    it is user registation page's view
    """
    form_class = UserRegisterForm
    template_name = 'user/registration_form.html'

    def get(self, request):
        """
        if request is of type get, it show the form
        :param request:
        :return:
        """
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        if request is of type post, it gets a form, verify it and save the user
        :param request:
        :return:
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            # Just for learning purposes, otherwise form.save() will save the data
            user = form.save(commit=False)
            # Just for learning purposes
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # return User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('my_user:index')

        return render(request, self.template_name, {'form': form})


class UserLoginFormView(View):
    """
    it is login page's view
    """
    form_class = UserLoginForm
    template_name = 'user/login_form.html'

    def get(self, request):
        """
        if request is of type get, it show the login form
        :param request:
        :return:
        """
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        if request is of type post, it gets form data, verify it and login the user
        :param request:
        :return:
        """
        form = self.form_class(request.POST)

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

        return render(request, self.template_name, {'form': form})


def logout_view(request):
    """
    it logs out the user
    :param request:
    :return:
    """
    logout(request)
    return redirect('my_user:index')


class UserEditFormView(View):
    """
    it is user edit profile page's view
    """
    form_class = UserEditForm
    template_name = 'user/edit_form.html'

    def get(self, request):
        """
        if request is of type get, it show the edit form
        :param request:
        :return:
        """
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        if request is of type post, it gets form data, verify it and update the user
        :param request:
        :return:
        """
        # to save the current instance and not create a new instance
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_user:index')

        return render(request, self.template_name, {'form': form})


class UserEditPassword(View):
    """
    it is user edit password page's view
    """
    form_class = UserChangePasswordForm
    template_name = 'user/change_password.html'

    def get(self, request):
        """
        if request is of type get, it show the password change form
        :param request:
        :return:
        """
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        if request is of type post, it gets form data, verify it and update the password
        :param request:
        :return:
        """
        # to save the current instance and not create a new instance
        form = self.form_class(user=request.user, data=request.POST)
        user = request.user
        if form.is_valid():
            password = request.POST['new_password1']
            user.set_password(password)
            user.save()
            return redirect('my_user:index')

        return render(request, self.template_name, {'form': form})
