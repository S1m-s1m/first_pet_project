# Generated by Django 5.0.3 on 2024-05-22 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created',), 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='order_item',
            options={'ordering': ('-pk',), 'verbose_name': 'Order item', 'verbose_name_plural': 'Order items'},
        ),
    ]
