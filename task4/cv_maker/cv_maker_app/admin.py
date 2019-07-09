# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import BasicInformation
from .models import Education
from .models import Experience

admin.site.register(BasicInformation)
admin.site.register(Experience)
admin.site.register(Education)
