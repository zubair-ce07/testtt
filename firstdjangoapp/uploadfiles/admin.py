from django.contrib import admin
from .models import Product, Category, Description, Skus, ImageUrls, Care


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Description)
admin.site.register(Skus)
admin.site.register(ImageUrls)
admin.site.register(Care)
