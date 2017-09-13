from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views import View, generic
from django.db.models.signals import pre_save
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions, permissions, generics as rest_generic

from user.models import Product, UserProfile
from user.forms import *
from user.serializers import *
from user.decorators import is_super_user, is_unauthenticated_user
from forms.permissions import IsOwner

USER = get_user_model()


@method_decorator(is_unauthenticated_user, 'dispatch')
class IndexView(View):

    def get(self, request):
        """
        redirect to sign up page, for loggedIn user redirect to
        new_product's page
        """
        return redirect(reverse('signup'))


@method_decorator(is_unauthenticated_user, 'dispatch')
class SignupView(View):

    def get(self, request, *args, **kwargs):
        """
        render sign up template with registration form,
        redirect to new_product page if already loggedIn
        """
        user_form = RegistrationForm()
        profile_form = UserProfileForm()
        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'signup.html', context)

    def post(self, request, *args, **kwargs):
        """
        register users after validating their forms data,
        redirect to new_product page if already loggedIn.
        """
        user_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data.get('password'))
            user.save(profile_form=profile_foview_product_rm)
            return redirect(reverse('login'))
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'signup.html', context)


@method_decorator(is_unauthenticated_user, 'dispatch')
class SignInView(View):

    def get(self, request, *args, **kwargs):
        """
        render login template with login form,
        redirect to new_product page if already loggedIn
        """
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request):
        """
        authenticate users, redirect to new_product page if already loggedIn
        """
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.current_user
            login(request, user)
            return redirect(reverse('new_product'))
        context = {'form': form}
        return render(request, 'login.html', context)


class NewProductView(LoginRequiredMixin, View):

    def get(self, request):
        """render new_product template along product creation form"""
        form = ProductForm()
        context = {'form': form}
        return render(request, 'new_product.html', context)

    def post(self, request):
        """create product object for inserted deatil for authenticated users"""
        form = ProductForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner_id = request.user.id
            item.save()
            return redirect(reverse('new_product'))


class ViewProductsView(LoginRequiredMixin, View):

    def get(self, request):
        """
        retrieves all user's list and render
        view_product template along user's list
        """
        users = USER.objects.all()
        context = {"item_list": [], "user_list": users, "user": None}
        return render(request, 'view_products.html', context)

    def post(self, request):
        """
        render view_product template along all user's list,
        product list of selected user and
        selected user's object
        """
        user_list = USER.objects.all()
        user = None
        products = []
        try:
            u_id = int(request.POST.get('user_id'))
            if u_id is not 0:
                user = USER.objects.get(id=u_id)
                products = user.products.all()
        except IndexError:
            pass
        except ObjectDoesNotExist:
            pass

        context = {
            "product_list": products,
            "user_list": user_list,
            "user": user
        }
        return render(request, 'view_products.html', context)


class ViewAllProductsView(LoginRequiredMixin, generic.TemplateView):
    """Template View to view all product"""
    template_name = 'view_all_products.html'

    def get_context_data(self, **kwargs):
        """
        retrieve all product's list
        :param kwargs: keyword arguments
        :returns context with all products list
        """
        context = super(ViewAllProductsView, self).get_context_data(**kwargs)
        context['products'] = models.Product.objects.all()
        return context


class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    """Generic detail view to show product's detail"""
    model = models.Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        """
        retrieve the product's owner
        :param kwargs: keyword arguments
        :returns context with owner's user object
        """
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        owner = USER.objects.get(id=self.get_object().owner_id)
        context['owner'] = owner
        return context


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    """Generic Detail View to show user's detail"""
    model = USER
    template_name = 'user_profile.html'


class SignoutView(View):

    def get(self, request):
        """logout loggedin user and redirects to login page"""
        logout(request)
        return redirect(reverse('login'))


@method_decorator(is_super_user, 'dispatch')
class UserListView(generic.ListView):
    """Generic List View to display all users list."""
    model = USER
    template_name = 'users_list.html'


class WithoutPasswordAuthticationView(View):

    def get(self, request, **kwargs):
        """authenticate users by only username"""
        username = self.kwargs.get('username')
        authenticated_user = authenticate(username=username)
        if authenticated_user:
            login(request, authenticated_user)
            return redirect(reverse('new_product'))
        return redirect(reverse('users_list'))


class UserListAPI(rest_generic.ListAPIView):
    """retrieves users list"""
    queryset = USER.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (permissions.IsAuthenticated, )


class TokenAuthenticationAPI(APIView):
    """authentication API: authenticate users"""
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, status = Token.objects.get_or_create(user=user)
            return Response({
                'status': True,
                'token': token.key,
                'id': user.id
            })
        return Response({
            'status': False,
            'token': None,
            'id': None
        })


class ProductListAPI(rest_generic.ListAPIView):
    """retrieves products list"""
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer


class UserProductListAPI(rest_generic.ListAPIView):
    """retrieves users products list"""

    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(owner_id=self.kwargs.get('owner'))


class ProductDetailAPI(rest_generic.RetrieveAPIView):

    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )


class UserProfileAPI(rest_generic.RetrieveAPIView):

    queryset = models.UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user'
    permission_classes = (permissions.IsAuthenticated, )


class CreateProductAPI(rest_generic.CreateAPIView):

    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )


class UpdateProductAPI(rest_generic.UpdateAPIView):

    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class SignUpAPI(rest_generic.CreateAPIView):

    serializer_class = UserProfileSerializer


class SignoutAPI(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response({
                "detail": "Successfully logged out.",
                "status": True
            },)
        except ObjectDoesNotExist:
            return Response({
                "detail": "Object Does Not Exist",
                "status": False
            },)
