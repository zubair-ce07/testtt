from django.contrib import admin
from .models import User

# registered custom used model with the admin app
admin.site.register(User)
