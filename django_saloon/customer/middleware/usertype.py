"""shop usertype middlwware"""
from django.shortcuts import redirect, reverse
from django.contrib import messages


class UserProfileRedirect:
    """Middleware for user profile.

        when profile is not completed,user will be redirected to profile page
        with a message to complete your profile"""

    def __init__(self, get_response):
        """init method of UserProfileredirect class"""
        self.get_response = get_response
        super(UserProfileRedirect, self).__init__()

    def __call__(self, request):
        """call method of UserProfileredirect class"""
        if not request.path == reverse('logout'):
            if hasattr(request.user, 'saloon') and request.user.saloon.shop_name == '':
                if not request.path == reverse('shop_profile'):
                    messages.warning(
                        request, f'Complete your profile first!')
                    return redirect(reverse('shop_profile'))
            if hasattr(request.user, 'customer') and request.user.customer.phone_no is None:
                if not request.path == reverse('customer_profile'):
                    messages.warning(
                        request, f'Complete your profile first!')
                    return redirect('customer_profile')

        return self.get_response(request)
