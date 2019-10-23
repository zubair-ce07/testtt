from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Product
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserCreationForm, SearchForm

class SignUpView(CreateView):
    """ This view class is to show Signup built in functionality."""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'main.html'

class ShowProducts(View):
    """ Display list of products."""
    products = Product.objects.all()
    
    @csrf_exempt
    def get(self, request):
        print('Nooo')
        page = request.GET.get('page', 1)

        paginator = Paginator(self.products, 4)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'home.html', {'user': request.user, 'products':products})
    @csrf_exempt
    def post(self, request):
        print('Yessssss')
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
