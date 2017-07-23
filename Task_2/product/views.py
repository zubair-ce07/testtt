from django.shortcuts import render
from django.views.generic.edit import View
from django.contrib.auth.mixins import LoginRequiredMixin

from product.models import Product, ImageURL, sku, ColorURL
from product.forms import CreateProductForm, ImageFormSet, ColorFormSet, skuFormSet


class CreateProductView(LoginRequiredMixin, View):
    form_class = CreateProductForm
    template_name = 'product/create_product.html'

    def get(self, request):
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
        # imageformset = ImageFormSet(instance=product)
        # colorformset = ColorFormSet(instance=product)
        # skuformset = skuFormSet(instance=product)
        if form.is_valid():

            pass
            # return HttpResponseRedirect('/success/')
        return render(request, self.template_name, {'form': form})

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
