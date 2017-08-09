# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from accounts.models import UserModel

admin.site.register(UserModel)
