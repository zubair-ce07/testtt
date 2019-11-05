""" Controller for Signup, Product and Order Pages """
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import Product, Order, OrderItems

from .forms import CustomUserCreationForm, SearchForm

class SignUpView(CreateView):
    """ This view class is to show Signup built in functionality."""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class ProductsList(ListView, FormView):
    """ Display list of products."""

    template_name = 'home.html'
    form_class = SearchForm
    context_object_name = 'products'
    paginate_by = 2
    queryset = Product.objects.all()

    def post(self, request):
        """ Filter to show products category wise. """
        form = SearchForm(request.POST)
        data = ''
        if form.is_valid():
            data = form.cleaned_data['category']
        products = Product.objects.filter(category=data)
        return render(request, 'home.html', {'text':data, 'products':products})


class OrderProducts(FormView):
    """ Class to save order details """

    success_url = '/'
    template_name = 'order.html'

    def get(self, request):
        """ Show form """
        return render(request, 'order.html')

    def post(self, request):
        """ Save values of all fields to database. """

        products = request.POST['items_id'].split(',')
        quantity = request.POST['items_quantity'].split(',')
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']
        phone = request.POST['phone']
        order = Order.objects.create(name=name, email=email, address=address, \
                    city=city, state=state, zip_code=zip_code, phone=phone)
        for count in range(len(quantity)):
            product = Product.objects.get(id=products[count])
            OrderItems.objects.create(order=order, product=product, \
                quantity=str(quantity[count]))
        return render(request, 'order.html')
