# Generated by Django 5.0.4 on 2024-04-13 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0006_remove_cart_name_remove_cart_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default='null', max_length=10),
        ),
        migrations.AddField(
            model_name='order',
            name='receiver',
            field=models.CharField(default='null', max_length=50),
        ),
    ]