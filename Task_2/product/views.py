from django.shortcuts import render
from django.views.generic.edit import View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy

from product.models import Product, ImageURL, SKU, ColorURL
from product.forms import CreateProductForm, ImageFormSet, ColorFormSet, skuFormSet


class CreateProductView(LoginRequiredMixin, View):
    form_class = CreateProductForm
    template_name = 'product/create_product.html'

    def get(self, request, *args, **kwargs):
        product = Product()
        form = self.form_class()
        imageformset = ImageFormSet(instance=product)
        colorformset = ColorFormSet(instance=product)
        skuformset = skuFormSet(instance=product)
        return render(request, self.template_name,
                      {'form': form, 'imageformset': imageformset, 'skuformset': skuformset,
                       'colorformset': colorformset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # skuformset.clean()
            #
            # skuform = sku(product=form.cleaned_data.get('product'),
            #               id='{}_{}'.format(form.cleaned_data.get('product').retailer_sku,
            #                                 form.cleaned_data.get('size')), size=form.cleaned_data.get('size'),
            #               price=form.cleaned_data.get('price'), color=form.cleaned_data.get('color'))
            # skuform.save()
            product = form.save()
            skuformset = skuFormSet(request.POST, instance=product)
            imageformset = ImageFormSet(request.POST, instance=product)
            colorformset = ColorFormSet(request.POST, instance=product)

            if imageformset.is_valid() and colorformset.is_valid() and skuformset.is_valid():
                imageformset.save()
                colorformset.save()
                skuformset.save()
        return HttpResponse('worked')


class EditProductView(LoginRequiredMixin, View):
    template_name = 'product/edit_product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        print(product)
        return render(request, self.template_name, {'product': product})

    def post(self, request, *args, **kwargs):
        pass



        # if skuformset.is_valid():
        #     skuformset.save()

        # return HttpResponseRedirect('/success/')


        # self.object = None
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)
        # image_form = imageformset()
        # iamge_formhelper = ImageFormHelper()
        #
        # return self.render_to_response(
        #     self.get_context_data(form=form, formset=image_form)
        # )

        # def post(self, request, *args, **kwargs):
        #     self.object = None
        #     form_class = self.get_form_class()
        #     form = self.get_form(form_class)
        #     image_form = imageformset(self.request.POST)
        #
        #     if form.is_valid() and image_form.is_valid():
        #         return self.form_valid(form, image_form)
        #
        #     return self.form_invalid(form, image_form)
        #
        # def form_valid(self, form, image_form):
        #     """
        #     Called if all forms are valid. Creates a Author instance along
        #     with associated books and then redirects to a success page.
        #     """
        #     self.object = form.save()
        #     image_form.instance = self.object
        #     image_form.save()
        #
        #     return HttpResponseRedirect(self.get_success_url())
        #
        # def form_invalid(self, form, image_form):
        #     return self.render_to_response(
        #         self.get_context_data(form=form, image_form=image_form)
        #     )
        #
        # def get_context_data(self, **kwargs):
        #     ctx = super(CreateProductView, self).get_context_data(**kwargs)
        #     image_formhelper = ImageFormHelper()
        #
        #     if self.request.POST:
        #         ctx['form'] = CreateProductForm(self.request.POST)
        #         ctx['image_form'] = imageformset(self.request.POST)
        #         ctx['image_formhelper'] = image_formhelper
        #     else:
        #         ctx['form'] = CreateProductForm()
        #         ctx['image_form'] = imageformset()
        #         ctx['image_formhelper'] = image_formhelper
        #
        #     return ctx


class DeleteProductView(LoginRequiredMixin, View):
    template_name = 'product/delete_product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        return render(request, self.template_name, {'product': product})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        Product.objects.get(pk=pk).delete()
        return render(request, reverse_lazy('search-product'))


class SearchProductView(LoginRequiredMixin, View):
    template_name = 'product/search_product.html'

    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            query = request.GET.get('q')
            context = {'query': query, 'error': True}
            if query:
                products = Product.objects.filter(name__icontains=query)
                context['products'] = products
                context['error'] = False
            return render(request, self.template_name, context)
        return render(request, self.template_name)
