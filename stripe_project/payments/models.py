from django.db import models


class Item(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    price = models.FloatField('Цена')
    stripe_price = models.CharField('Цена на stripe.com', max_length=50, blank=True, null=True,)

    def __str__(self):
        return f'{self.name} цена: {self.price}'

class Order(models.Model):
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    items = models.ManyToManyField(Item)
