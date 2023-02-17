from django.contrib import admin

from .models import Discount, Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "description", "price")
    search_fields = ("name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "created", "discount")


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("pk", "stripe_id", "percentage_discount")
