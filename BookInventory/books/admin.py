# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from books.models import Author, Publisher, Book, UserModel

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(UserModel)