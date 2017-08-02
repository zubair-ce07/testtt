from __future__ import unicode_literals

from django.shortcuts import redirect


def index(request):
    return redirect('/books')
