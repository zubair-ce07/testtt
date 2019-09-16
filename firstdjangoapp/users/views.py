from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.views import View

from .forms import ProfileUpdateForm, SignUpForm, UserUpdateForm


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
            return redirect('/shopcity/profile')


class CartView(View):
    template_name = "cart.html"

    def get(self, request):
        context = {}
        if hasattr(request.user, 'cart'):
            cart_items = request.user.cart.cart_items.all()
            cart_total = 0
            for cart_item in cart_items:
                cart_total += (cart_item.product.skus.get(sku_id=cart_item.sku_id).price * cart_item.quantity)
            context = {
                "cart_items": cart_items.all(),
                "number_of_products": cart_items.aggregate(Sum('quantity'))['quantity__sum'],
                "cart_total": cart_total
            }
        return render(request, self.template_name, context)

    def post(self, request):
        cart_items = request.user.cart.cart_items.all()
        cart_items.filter(product__retailer_sku=request.POST['id']).delete()
        context = {}
        if hasattr(request.user, 'cart'):
            cart_total = 0
            for cart_item in cart_items:
                cart_total += (cart_item.product.skus.get(sku_id=cart_item.sku_id).price * cart_item.quantity)
            context = {
                "cart_items": cart_items.all(),
                "number_of_products": cart_items.aggregate(Sum('quantity'))['quantity__sum'],
                "cart_total": cart_total
            }
        return render(request, self.template_name, context)
