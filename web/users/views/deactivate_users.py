from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View
from web.users.models import User


class DeactivateUsersView(View):

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        #TODO: please remove the for loop and make the code more efficient by using only single query of filter and update.
        #TODO: Please try not to use semicolon.
        users = User.objects.all();
        for user in users:
            if user.is_active and not user.is_staff:
                user.is_active = False
                user.save()

        return redirect(reverse('admin:index'))
