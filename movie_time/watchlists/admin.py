from django.contrib import admin
from watchlists.models import *


admin.site.register([WatchListItem, Activity])
