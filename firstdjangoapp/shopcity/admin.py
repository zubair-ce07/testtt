from django.contrib import admin

from .models import Category, Product, Skus


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Skus)
