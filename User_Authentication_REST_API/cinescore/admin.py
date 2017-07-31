from django.contrib import admin
from .models import Movie, UserRating, Category, Website, Rating

admin.site.register(Movie)
admin.site.register(UserRating)
admin.site.register(Category)
admin.site.register(Website)
admin.site.register(Rating)
