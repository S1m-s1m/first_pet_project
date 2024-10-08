# Generated by Django 5.0.3 on 2024-05-13 12:52

import django.core.validators
import django.db.models.deletion
import parler.fields
import parler.models
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='brand_images/')),
            ],
            options={
                'ordering': ('-pk',),
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('size', models.CharField(choices=[('XXS', 'XX Small'), ('XS', 'X Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'X Large'), ('XXL', 'XX Large'), ('XXXL', 'XXX Large')], default='M', max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='clothes_images/')),
                ('availability', models.BooleanField()),
                ('created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created',),
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='text')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='date')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='name')),
                ('description', models.CharField(max_length=500)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='catalog.category')),
            ],
            options={
                'verbose_name': 'category Translation',
                'db_table': 'catalog_category_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='ProductTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('slug', models.SlugField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='category')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='catalog.product')),
            ],
            options={
                'verbose_name': 'product Translation',
                'db_table': 'catalog_product_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
    ]
