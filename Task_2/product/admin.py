from django.contrib import admin

from product.models import Product, ImageURL, sku, ColorURL


class ImageURLInline(admin.StackedInline):
    model = ImageURL
    extra = 1


class ColorURLInline(admin.StackedInline):
    model = ColorURL
    extra = 1


class skuInline(admin.StackedInline):
    model = sku
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ImageURLInline, ColorURLInline, skuInline)
    list_display = ('name', 'brand',)
