from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View
from web.users.models import User


class ActivateUsersView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        User.objects.filter(is_admin=False, is_active=False).update(is_active=True)
        return redirect(reverse('admin:index'))