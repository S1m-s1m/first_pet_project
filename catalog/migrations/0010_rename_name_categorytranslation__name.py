# Generated by Django 5.0.3 on 2024-05-14 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_product_brand_alter_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categorytranslation',
            old_name='name',
            new_name='_name',
        ),
    ]
