from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from django.template import loader, Context


class UserProfileRedirect(object):

    def __init__(self, get_response):
        self.get_response = get_response
        super(UserProfileRedirect, self).__init__()

    def __call__(self, request):
        if not request.path == reverse('logout'):
            if hasattr(request.user, 'saloon') and request.user.saloon.shop_name == '':
                if not request.path == reverse('shop_profile'):
                    return redirect(reverse('shop_profile'))
            if hasattr(request.user, 'customer') and request.user.customer.phone_no == None:
                if not request.path == reverse('customer_profile'):
                    return redirect('customer_profile')

        return self.get_response(request)
