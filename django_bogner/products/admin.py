from django.contrib import admin
from .models import Product, Category, Sku, Image

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Sku)
admin.site.register(Image)
