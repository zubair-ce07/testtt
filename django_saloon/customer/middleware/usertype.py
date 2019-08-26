from django.shortcuts import redirect, reverse
from django.contrib import messages


class UserProfileRedirect(object):

    def __init__(self, get_response):
        self.get_response = get_response
        super(UserProfileRedirect, self).__init__()

    def __call__(self, request):
        if not request.path == reverse('logout'):
            if hasattr(request.user, 'saloon') and request.user.saloon.shop_name == '':
                if not request.path == reverse('shop_profile'):
                    messages.warning(
                        request, f'Complete your profile first!')
                    return redirect(reverse('shop_profile'))
            if hasattr(request.user, 'customer') and request.user.customer.phone_no == None:
                if not request.path == reverse('customer_profile'):
                    messages.warning(
                        request, f'Complete your profile first!')
                    return redirect('customer_profile')

        return self.get_response(request)
