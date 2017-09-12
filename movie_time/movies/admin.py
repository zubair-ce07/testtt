from django.contrib import admin
from movies.models import *


admin.site.register([Movie, Video, Image, Role, Job, Person, Date, Genre])
