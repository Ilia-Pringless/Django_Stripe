import stripe
from django.conf import settings
from django.db.models import Sum
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from .models import Discount, Item, Order


class ItemPageView(TemplateView):
    """Отображение страницы товара"""

    template_name = "item.html"

    def get_context_data(self, **kwargs):
        item = Item.objects.get(id=self.kwargs["item_id"])
        context = super(ItemPageView, self).get_context_data(**kwargs)
        discount = item.discount if item.discount else 0
        final_price = item.price - (item.price / 100 * int(discount.__str__()))
        context.update(
            {
                "item": item,
                "discount": discount,
                "final_price": final_price,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLISHABLE_KEY,
            }
        )
        return context


class OrderPageView(TemplateView):
    """Отображение страницы заказа"""

    template_name = "order.html"

    def get_context_data(self, **kwargs):
        order_id = self.kwargs["order_id"]
        order = Order.objects.get(id=order_id)
        items = order.items
        total = items.aggregate(Sum("price"))["price__sum"]
        discount = order.discount if order.discount else 0
        final_price = total - (total / 100 * int(discount.__str__()))
        context = super(OrderPageView, self).get_context_data(**kwargs)
        context.update(
            {
                "order_id": order_id,
                "discount": discount,
                "final_price": final_price,
                "items": items,
                "total": total,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLISHABLE_KEY,
            }
        )
        return context


@csrf_exempt
def send_order_payment(request, id):
    """Кнопка отправки заказа на оплату"""
    if request.method == "GET":
        stripe.api_key = settings.STRIPE_SECRET_KEY
        line_items = generate_line_items(path=request.path, obj_id=id)
        discount = get_discount(path=request.path, obj_id=id)
        try:
            return create_checkout_session(line_items=line_items, discount=discount)
        except Exception as err:
            return JsonResponse({"error": str(err)})


def generate_line_items(path: str, obj_id: int) -> list:
    """Создание списка товаров для оплаты"""
    if "/buy_order" in path:  # если страница оплаты заказа
        items = Order.objects.get(id=obj_id).items
        line_items = [
            {"price": item.stripe_price, "quantity": 1} for item in items.all()
        ]
        return line_items
    elif "buy/" in path:  # если страница оплаты отдельного товара
        item = Item.objects.get(id=obj_id)
        line_items = [{"price": item.stripe_price, "quantity": 1}]
        return line_items


def get_discount(path: str, obj_id: int) -> str | None:
    """Получить скидку (при наличии)"""
    if "/buy_order" in path:
        try:
            return Discount.objects.get(order=obj_id).stripe_id
        except Discount.DoesNotExist:
            return None
    elif "buy/" in path:
        try:
            return Discount.objects.get(item=obj_id).stripe_id
        except Discount.DoesNotExist:
            return None


def create_checkout_session(line_items: list, discount: str | None) -> JsonResponse:
    """Создание сессии для оплаты"""
    domain_url = "http://localhost:8000/"
    checkout_session = stripe.checkout.Session.create(
        success_url=domain_url + "success",
        line_items=line_items,
        mode="payment",
        discounts=[{"coupon": discount}],
    )
    return JsonResponse({"id": checkout_session["id"]})
