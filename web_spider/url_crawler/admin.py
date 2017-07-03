from django.contrib import admin
from .models import Link, WebPage


# registering models to admin site
admin.site.register(WebPage)
admin.site.register(Link)
