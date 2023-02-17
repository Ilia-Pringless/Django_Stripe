from django.urls import path

from . import views

urlpatterns = [
    path("buy/<int:id>", views.send_order_payment, name="buy_item"),
    path("buy_order/<int:id>", views.send_order_payment, name="buy_order"),
    path("item/<int:item_id>", views.ItemPageView.as_view(), name="item"),
    path("order/<int:order_id>", views.OrderPageView.as_view(), name="order"),
]
