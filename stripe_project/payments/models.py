from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Discount(models.Model):
    stripe_id = models.CharField('ID на stripe.com', max_length=50)
    percentage_discount = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )

    def __str__(self):
        return f'{self.percentage_discount}'


class Item(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    price = models.FloatField('Цена')
    stripe_price = models.CharField(
        'Цена на stripe.com', max_length=50, blank=True, null=True
    )
    discount = models.ForeignKey(
        Discount, related_name="item", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f'{self.name} цена: {self.price}'


class Order(models.Model):
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(
        Discount, related_name='order', on_delete=models.SET_NULL, blank=True, null=True
    )
