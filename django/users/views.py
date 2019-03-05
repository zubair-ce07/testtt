from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from .forms import UserForm
from .forms import ProfileForm

from .models import Profile


class SignUpView(View):
    template_name = 'registration/userform.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'user_form': UserForm(),
            'profile_form': ProfileForm(),
            'title': 'Sign up'
        })

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': 'Sign up'
        })


@method_decorator(login_required, name='dispatch')
class UpdateUserView(View):
    template_name = 'registration/userform.html'

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        user_form.fields['password1'].required = False
        user_form.fields['password2'].required = False
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': ProfileForm(instance=request.user.profile),
            'title': 'Update'
        })

    def post(self, request, *args, **kwargs):
        password_changed = False
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        user_form.fields['password1'].required = False
        user_form.fields['password2'].required = False

        if user_form.is_valid() and profile_form.is_valid():
            user = request.user
            if user_form.cleaned_data['password1']:
                user.set_password(user_form.cleaned_data['password1'])
                password_changed = True

            user.username = user_form.cleaned_data['username']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.profile.role = profile_form.cleaned_data['role']
            user.save()

            if password_changed:
                update_session_auth_hash(request, user)

            return redirect('home')

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': 'Update'
        })
