# Generated by Django 4.1.6 on 2023-02-17 09:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0008_alter_order_discount_alter_order_tax"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="tax",
        ),
        migrations.DeleteModel(
            name="Tax",
        ),
    ]
