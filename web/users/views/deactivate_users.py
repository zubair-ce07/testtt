from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View
from web.users.models import User


class DeactivateUsersView(View):

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        User.objects.filter(is_admin=False, is_active=True).update(is_active=False)
        return redirect(reverse('admin:index'))
