# Generated by Django 5.0.7 on 2024-08-03 08:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_item',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order', verbose_name='order'),
        ),
    ]
