# Generated by Django 5.0.3 on 2024-05-22 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_alter_brand_options_alter_brandtranslation_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorytranslation',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='name'),
        ),
    ]
