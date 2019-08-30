from django.contrib import admin

from .models import Brand, Category, Product, ProductArticle, ProductImage


class ProductArticleAdmin(admin.TabularInline):
    model = ProductArticle


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductArticleAdmin, ProductImageAdmin]
    search_fields = ['category__name']


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

