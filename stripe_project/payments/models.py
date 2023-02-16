from django.db import models


class Item(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    price = models.FloatField('Цена')

    def __str__(self):
        return f'{self.name} цена: {self.price}'

class Order(models.Model):
    # items = models.ForeignKey(
    #     Item,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='order',
    #     verbose_name='Заказ',
    # )
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    items = models.ManyToManyField(Item)
