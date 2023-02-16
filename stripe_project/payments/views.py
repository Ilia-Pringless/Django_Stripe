from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Order
from django.db.models import Sum
import stripe


class IndexPageView(TemplateView):
    template_name = 'purchase.html'

    def get_context_data(self, **kwargs):
        item = Item.objects.get(id=self.kwargs["item_id"])
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context.update({
            "item": item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLISHABLE_KEY
        })
        return context


class OrderPageView(TemplateView):
    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        order_id = self.kwargs["order_id"]
        items = Order.objects.get(id=order_id).items
        total = items.aggregate(Sum('price'))['price__sum']
        context = super(OrderPageView, self).get_context_data(**kwargs)
        context.update({
            'order_id': order_id,
            'items': items,
            'total': total,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY
        })
        return context


@csrf_exempt
def send_order_payment(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        line_items
        try:
            create_checkout_session(line_items)
        except Exception as err:
            return JsonResponse({'error': str(err)})


def create_checkout_session(line_items: list):
    checkout_session = stripe.checkout.Session.create(
        success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',  # сделать страничку успеха
        # cancel_url=domain_url + 'cancelled/',  # и неуспеха
        line_items=[
            {
                'price': 'price_1MbpqqGVl5Wd7WlmOi4KrWog',
                'quantity': 1,
            },
        ],
        mode='payment'
    )
    return JsonResponse({'id': checkout_session['id']})