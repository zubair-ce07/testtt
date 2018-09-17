from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, \
    PasswordChangeForm
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserEditForm
from .serializer import UserRegisterSerializer, UserLoginSerializer, UserEditSerializer, \
    UserEditPasswordSerializer


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

# ##################################################################################################
# Below are the same views with REST framework
class RestIndexView(APIView):
    template_name = 'user/index.html'
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        return Response({'is_rest':True})


class RestUserFormView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'user/registration_form.html'

    def get(self, request):
        serializer = UserRegisterSerializer(None)
        return Response({'serializer': serializer, 'is_rest':True})

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'is_rest':True})

        serializer.save()
        username = request.data['username']
        password = request.data['password1']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
        return redirect('my_user:rest_index')


class RestUserLoginFormView(APIView):
    # form_class = AuthenticationForm
    template_name = 'user/login_form.html'
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        serializer = UserLoginSerializer(None)
        return Response({'serializer': serializer, 'is_rest':True})

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            error = "Please enter a valid username or password"
            return Response({'serializer': serializer, 'error_message': error, 'is_rest':True})
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('my_user:rest_index')
            else:
                error = "Your account is inactive. Kindly contact the admin"
                return Response({'serializer': serializer, 'error_message': error, 'is_rest':True})
        else:
            error = "Please enter a valid username or password"
            return Response({'serializer': serializer, 'error_message': error, 'is_rest':True})


def rest_logout_view(request):
    logout(request)
    return redirect('my_user:rest_index')


class RestUserEditFormView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'user/edit_form.html'

    def get(self, request):
        serializer = UserEditSerializer(request.user)
        return Response({'serializer': serializer, 'is_rest':True})

    def post(self, request):
        serializer = UserEditSerializer(request.user, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'is_rest':True})

        serializer.save()
        return redirect('my_user:rest_index')


class RestUserEditPassword(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'user/change_password.html'

    def get(self, request):
        serializer = UserEditPasswordSerializer(None)
        return Response({'serializer': serializer, 'is_rest':True})

    def post(self, request):
        serializer = UserEditPasswordSerializer(request.user, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'is_rest':True})

        serializer.save()
        return redirect('my_user:rest_index')