from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Order
from django.db.models import Sum
import stripe


class IndexPageView(TemplateView):
    """Отображение страницы товара"""
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        item = Item.objects.get(id=self.kwargs['item_id'])
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context.update({
            'item': item,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY
        })
        return context


class OrderPageView(TemplateView):
    """Отображение страницы заказа"""
    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        order_id = self.kwargs['order_id']
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
def send_order_payment(request, id: int):
    """Кнопка отправки заказа на оплату"""
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        line_items = generate_line_items(path=request.path, obj_id=id)
        try:
            return create_checkout_session(line_items=line_items)
        except Exception as err:
            return JsonResponse({'error': str(err)})


def generate_line_items(path: str, obj_id: int) -> list:
    """Создание списка товаров для оплаты"""
    if '/buy_order' in path:  # если страница оплаты заказа
        items = Order.objects.get(id=obj_id).items
        line_items = [{'price': item.stripe_price, 'quantity': 1} for item in items.all()]
        return line_items
    elif 'buy/' in path:  # если страница оплаты отдельного товара
        item = Item.objects.get(id=obj_id)
        line_items = [{'price': item.stripe_price, 'quantity': 1}]
        return line_items


def create_checkout_session(line_items: list) -> JsonResponse:
    """Создание сессии для оплаты"""
    domain_url = 'http://localhost:8000/'
    checkout_session = stripe.checkout.Session.create(
        success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',  # сделать страничку успеха
        # cancel_url=domain_url + 'cancelled/',  # и неуспеха
        line_items=line_items,
        mode='payment'
    )
    return JsonResponse({'id': checkout_session['id']})
