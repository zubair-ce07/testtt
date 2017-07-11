from django.contrib import admin
from .models import Product, Images, Skus, Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    fields = ('name', 'brand_link', 'image_icon', 'image_tag',)
    readonly_fields = ('image_tag',)


class ImageInLine(admin.TabularInline):
    model = Images


class SkusInLine(admin.TabularInline):
    model = Skus


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'category', 'entry_date', 'update_date')
    search_fields = ('product_id', 'product_name', 'category')
    list_filter = ('entry_date', 'update_date')
    ordering = ('-entry_date',)
    fields = ('brand', 'product_id', 'product_name', 'category', 'source_url')

    inlines = [
        ImageInLine,
        SkusInLine
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
admin.site.register(Skus)
admin.site.register(Brand, BrandAdmin)
