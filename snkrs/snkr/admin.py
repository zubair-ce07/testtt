from django.contrib import admin

from snkr.models import Description, ImageUrls, Skus, Snkr

admin.site.register(Snkr)
admin.site.register(ImageUrls)
admin.site.register(Skus)
admin.site.register(Description)
