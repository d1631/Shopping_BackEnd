# Generated by Django 3.2.8 on 2022-12-17 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_products', '0002_alter_product_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
    ]
