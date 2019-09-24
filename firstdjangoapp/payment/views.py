import stripe
from django.conf import settings
from django.shortcuts import render
from django.views import View

from .models import Payment


stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentView(View):
    template_name = 'payment.html'

    def get(self, request, *args, **kwargs):
        context = request.user.cart.get(state='Current').as_dict()
        context["cart_total_gbp"] = float(context['cart_total']) / 100.0
        context["key"] = settings.STRIPE_PUBLISHABLE_KEY
        return render(request, self.template_name, context)


class ChargeView(View):
    template_name = 'charge.html'

    def post(self, request):
        cart = request.user.cart.get(state='Current')
        context = cart.as_dict()
        charge = stripe.Charge.create(
            amount=context['cart_total'],
            currency='gbp',
            description='ShopCity Payment',
            source=request.POST['stripeToken'],
            metadata={
                'username': request.user.username,
                'order_number': cart.id
            }
        )
        payment = Payment(user=request.user, cart=cart, status=charge['status'])
        payment.save()
        if charge['status'] == 'succeeded':
            request.user.cart.filter(state='Current').update(state='Processed')
        else:
            request.user.cart.filter(state='Current').update(state='Canceled')
        context['cart_total'] = float(context['cart_total']) / 100.0
        context['status'] = charge['status']
        return render(request, self.template_name, context)
