from django.contrib import admin
from django.contrib.auth.models import Group
from url_crawler.models import CustomUser, Link, WebPage


# registering models to admin site
admin.site.register(WebPage)
admin.site.register(Link)
admin.site.register(CustomUser)

# un register unused model from admin site
admin.site.unregister(Group)
