"""
this module contains the views of this django app
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserEditForm
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserEditSerializer, \
    UserEditPasswordSerializer


class IndexView(TemplateView):
    """
    this is TemplateView of Index page
    """
    template_name = 'user/index.html'


class UserFormView(View):
    """
        it is user registation page's view
    """
    form_class = UserCreationForm
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
            password = form.cleaned_data['password1']
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
    form_class = AuthenticationForm
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
        form = self.form_class(instance=request.user, )
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
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'

    def get(self, request):
        """
        if request is of type get, it show the password change form
        :param request:
        :return:
        """
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        if request is of type post, it gets form data, verify it and update the password
        :param request:
        :return:
        """
        # to save the current instance and not create a new instance
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_user:index')

        return render(request, self.template_name, {'form': form})


# ##################################################################################################
# Below are the same views with REST framework
class RestIndexView(APIView):
    """
    this is a View of Index page with DRF
    """
    template_name = 'user/index.html'
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        """
        it displays index page with DRF
        :param request:
        :return:
        """
        return Response({'is_rest': True})


class RestUserFormView(APIView):
    """
    it is user registation page's view with DRF
    """
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'user/registration_form.html'

    def get(self, request):
        """
        if request is of type get, it shows the registration form but this form is serializer form
         of DRF
        :param request:
        :return:
        """
        serializer = UserRegisterSerializer(None)
        return Response({'serializer': serializer, 'is_rest': True})

    def post(self, request):
        """
        if request is of type post, it gets the serializer form, verify it and save the user
        :param request:
        :return:
        """
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'is_rest': True})

        serializer.save()
        username = request.data['username']
        password = request.data['password1']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
        return redirect('my_user:rest_index')


class RestUserLoginFormView(APIView):
    """
    it is login page's view with DRF
    """
    template_name = 'user/login_form.html'
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        """
        if request is of type get, it show the login form but this form is serializer form
         of DRF
        :param request:
        :return:
        """
        serializer = UserLoginSerializer(None)
        return Response({'serializer': serializer, 'is_rest': True})

    def post(self, request):
        """
        if request is of type post, it gets form data, verify it and login the user
        :param request:
        :return:
        """
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            error = "Please enter a valid username or password"
            return Response({'serializer': serializer, 'error_message': error, 'is_rest': True})
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('my_user:rest_index')
            else:
                error = "Your account is inactive. Kindly contact the admin"
                return Response({'serializer': serializer, 'error_message': error, 'is_rest': True})
        else:
            error = "Please enter a valid username or password"
            return Response({'serializer': serializer, 'error_message': error, 'is_rest': True})


def rest_logout_view(request):
    """
    it logs out the user and redirect user to RestIndex
    :param request:
    :return:
    """
    logout(request)
    return redirect('my_user:rest_index')


class RestUserEditFormView(APIView):
    """
    it is user edit profile page's view with DRF
    """
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'user/edit_form.html'

    def get(self, request):
        """
        if request is of type get, it show the edit form but this form is serializer form
         of DRF
        :param request:
        :return:
        """
        serializer = UserEditSerializer(request.user)
        return Response({'serializer': serializer, 'is_rest': True})

    def post(self, request):
        """
        if request is of type post, it gets form data, verify it and update the user
        :param request:
        :return:
        """
        serializer = UserEditSerializer(request.user, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'is_rest': True})

        serializer.save()
        return redirect('my_user:rest_index')


class RestUserEditPassword(APIView):
    """
    it is user edit password page's view with DRF
    """
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'user/change_password.html'

    def get(self, request):
        """
        if request is of type get, it show the password change form but this form is serializer form
         of DRF
        :param request:
        :return:
        """
        serializer = UserEditPasswordSerializer(None)
        return Response({'serializer': serializer, 'is_rest': True})

    def post(self, request):
        """
        if request is of type post, it gets form data, verify it and update the password
        :param request:
        :return:
        """
        serializer = UserEditPasswordSerializer(request.user, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'is_rest': True})

        serializer.save()
        return redirect('my_user:rest_index')
