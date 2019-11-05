""" Controller for manager's profile. """

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from .models import Product
from .forms import ProductsAction
from users.forms import ProductForm


class Home(ListView, FormView):
    """ Show products on manager's profile category wise. """

    template_name = 'index.html'
    paginate_by = 5
    form_class = ProductsAction
    context_object_name = 'products'
    queryset = Product.objects.all()

    def post(self, request):
        """ Perform multiple actions on products. """

        form = ProductsAction(request.POST)
        if form.is_valid():
            if 'delete' in request.POST:
                for item in request.POST.getlist('choices'):
                    Product.objects.filter(id=item).delete()
            if 'price' in request.POST:
                for item in request.POST.getlist('choices'):
                    Product.objects.filter(id=item).update(price=request.POST.get('price'))

        return render(request, self.template_name)


class AddProduct(FormView):
    """ Add product functionality. """

    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = '/'

    def post(self, request):
        """ Save all fields to db to add a product. """

        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        category = request.POST['category']
        pub_date = request.POST['pub_date']
        image = 'users/images/'+ request.POST['image']

        if Product.objects.filter(name=name).exists():
            Product.objects.filter(name=name).update(price=price, \
                description=description, category=category, image=image, \
                pub_date=pub_date)
        else:
            product = Product(name=name, price=price, category=category, \
            description=description, image=image, pub_date=pub_date)
            product.save()
        return render(request, 'add_product.html')
