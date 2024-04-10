# Generated by Django 5.0.4 on 2024-04-09 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0002_cart_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='id_medicine',
            new_name='medicine',
        ),
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]