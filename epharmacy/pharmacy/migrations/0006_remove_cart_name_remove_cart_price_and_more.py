# Generated by Django 5.0.4 on 2024-04-11 19:10

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
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
        migrations.AddField(
            model_name='medicine',
            name='discount_price',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='medicine',
            name='image2',
            field=models.ImageField(default=None, upload_to='medicine/%y/%m'),
        ),
        migrations.AddField(
            model_name='medicine',
            name='image3',
            field=models.ImageField(default=None, upload_to='medicine/%y/%m'),
        ),
        migrations.AddField(
            model_name='medicine',
            name='image4',
            field=models.ImageField(default=None, upload_to='medicine/%y/%m'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.CreateModel(
            name='OfferProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('is_active', models.BooleanField(default=True)),
                ('medicine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='category_offers', to='pharmacy.medicine')),
            ],
        ),
    ]
