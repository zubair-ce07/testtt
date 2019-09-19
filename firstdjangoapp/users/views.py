from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views import View

from .forms import ProfileUpdateForm, SignUpForm, UserUpdateForm
from .models import Profile


class SignUpView(View):
    template_name = "signup.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully!!')
            user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
            profile, created = Profile.objects.get_or_create(user=user)
            if user:
                login(request, user)
                return redirect('/shopcity/search/')
            return render(request, self.template_name, {'form': AuthenticationForm(request.POST)})
        return render(request, self.template_name, {'form': form})


class ProfileView(View):

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, "profile.html", context)

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account Updated!!!')
            return redirect('/user/profile')
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, "profile.html", context)


class CartView(View):
    template_name = "cart.html"

    def get(self, request):
        context = {}
        if request.user.cart.filter(state='Current').exists():
            context = request.user.cart.get(state='Current').as_dict()
        return render(request, self.template_name, context)

    def post(self, request):
        cart = request.user.cart.get(state='Current')
        cart_items = cart.cart_items.all()
        cart_items.filter(product__retailer_sku=request.POST['id']).delete()
        context = cart.as_dict()
        return render(request, self.template_name, context)
