import django.dispatch

user_login = django.dispatch.Signal(providing_args=['user_name'])
user_logout = django.dispatch.Signal(providing_args=['user_name'])