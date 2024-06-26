# Generated by Django 5.0.4 on 2024-04-16 07:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0010_alter_offerproduct_options_and_more'),
    ]

    operations = [

        migrations.AlterModelOptions(
            name='offerproduct',
            options={},
        ),
        migrations.AlterField(
            model_name='medicine',
            name='discount_price',
            field=models.DecimalField(decimal_places=3, editable=False, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.DeleteModel(
            name='DetailInvoice',
        ),
        migrations.CreateModel(
            name='DrugType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.category')),
            ],
        ),
    ]
