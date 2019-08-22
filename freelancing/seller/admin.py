from django.contrib import admin

# Register your models here.
from .models import Category, SearchTag, Gig, Package, Faq, Requirements
admin.site.register(Category)
admin.site.register(SearchTag)
admin.site.register(Gig)
admin.site.register(Package)
admin.site.register(Faq)
admin.site.register(Requirements)
