# Generated by Django 4.1.6 on 2023-02-16 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_order_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stripe_price',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Цена на stripe.com'),
        ),
    ]
