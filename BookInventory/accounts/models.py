# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, UserManager
from django.db import models


class UserModel(User):
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    address = models.CharField(max_length=512, blank=True)
    contact = models.CharField(max_length=32, blank=True)
    timezone = models.CharField(max_length=64, default='Asia/Karachi')
    objects = UserManager()
