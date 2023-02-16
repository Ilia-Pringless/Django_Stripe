from django.urls import path

from . import views

urlpatterns = [
    path('buy/1', views.create_checkout_session),
    path('item/<int:item_id>', views.IndexPageView.as_view(), name='index'),
    path('order/<int:order_id>', views.OrderPageView.as_view(), name='order')
]
