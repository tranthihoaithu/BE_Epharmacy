# Generated by Django 5.0.4 on 2024-04-09 17:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0005_alter_cart_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='name',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
        migrations.AlterField(
            model_name='medicine',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
