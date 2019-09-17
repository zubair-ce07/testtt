import stripe
from django.conf import settings
from django.shortcuts import render
from django.views import View

from .models import Payment
from users.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentView(View):
    template_name = 'payment.html'

    def get(self, request, *args, **kwargs):
        context = request.user.cart.as_dict()
        context["cart_total_gbp"] = float(context['cart_total']) / 100.0
        context["key"] = settings.STRIPE_PUBLISHABLE_KEY
        return render(request, self.template_name, context)


class ChargeView(View):
    template_name = 'charge.html'

    def post(self, request):
        context = request.user.cart.as_dict()
        order = Order(user=request.user, order_total=context['cart_total'])
        order.save()
        for cart_item in context['cart_items']:
            order_item = OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                sku_id=cart_item.sku_id,
                sku_price=cart_item.sku_price,
                sku_size=cart_item.sku_size,
                sku_colour=cart_item.sku_colour
            )
            order_item.save()
        charge = stripe.Charge.create(
            amount=context['cart_total'],
            currency='gbp',
            description='ShopCity Payment',
            source=request.POST['stripeToken']
        )
        payment = Payment(user=request.user, order=order, status=charge['status'])
        payment.save()
        request.user.cart.delete()
        context['cart_total'] = float(context['cart_total']) / 100.0
        return render(request, self.template_name, context)
