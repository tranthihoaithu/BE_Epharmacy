# Generated by Django 5.0.4 on 2024-04-22 19:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0018_remove_medicine_subcategory_and_more'),
    ]

    operations = [

        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=None, upload_to='upload/%y'),
        ),

    ]