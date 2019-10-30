from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Product, Order, CustomUser
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import CustomUserCreationForm, SearchForm

class SignUpView(CreateView):
    """ This view class is to show Signup built in functionality."""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class ShowProducts(View):
    """ Display list of products."""
    products = Product.objects.all()
    print(products)

    def get(self, request):
        """ Show list of all products in pagination """
        page = request.GET.get('page', 1)

        paginator = Paginator(self.products, 4)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'home.html', {'user': request.user, 'products':products})


    def post(self, request):
        """ Filter to show products category wise """
        form = SearchForm(request.POST)
        data = ''
        if form.is_valid():
            data = form.cleaned_data['category']
        products = Product.objects.filter(category=data)
        page = request.GET.get('page', 1)

        paginator = Paginator(products, 4)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'home.html', {'text':data, 'products':products})


class OrderProducts(View):
    """ Class to save order details """
    def get(self, request):
        """ Show form """
        return render(request, 'order.html')

    def post(self, request):
        """Save values of all fields to database """
        if request.method == "POST":
            products = request.POST['items_json']
            name = request.POST['name']
            email = request.POST['email']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip']
            phone = request.POST['phone']
            order = Order(products=products, name=name, email=email, address=address,
                          city=city, state=state, zip_code=zip_code,
                          phone=phone)
            order.save()
        return render(request, 'order.html')
