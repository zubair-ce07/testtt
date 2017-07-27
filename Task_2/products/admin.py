from django.contrib import admin

from products.models import Product, ImageURL, Sku, ColorURL, DateTime


class ImageURLInline(admin.StackedInline):
    model = ImageURL
    extra = 1


class ColorURLInline(admin.StackedInline):
    model = ColorURL
    extra = 1


class SkuInline(admin.StackedInline):
    model = Sku
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ImageURLInline, ColorURLInline, SkuInline)
    list_display = ('name', 'url',)

@admin.register(DateTime)
class DateTime(admin.ModelAdmin):
    list_display = ('datetime', 'timezone')
