from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View
from web.users.models import User


class ActivateUsersView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):

        users = User.objects.all();
        for user in users:
            if not user.is_active and not user.is_staff:
                user.is_active = True
                user.save()

        return redirect(reverse('admin:index'))