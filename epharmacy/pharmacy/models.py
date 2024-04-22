from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from ckeditor.fields import RichTextField
from django.core.serializers import serialize
from django.db.models import OuterRef, Subquery
import json


class User(AbstractUser):
    avatar = models.ImageField(upload_to='upload/%y/%m/%d/', blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, null=False)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='upload/%y', default=None)

    def __str__(self):
        return self.name

    def get_children(self):
        return Category.objects.filter(parent=self)

    
class Unit(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, null=False)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    id_medicine = models.CharField(max_length=20, unique=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    name_medicine = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='medicine/%y/%m', default=None)
    image2 = models.ImageField(upload_to='medicine/%y/%m', default=None)
    image3 = models.ImageField(upload_to='medicine/%y/%m', default=None)
    image4 = models.ImageField(upload_to='medicine/%y/%m', default=None)
    trademark = models.CharField(max_length=100)
    stock_quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)], null=True, editable=False)
    uses = models.CharField(max_length=100)
    object = models.CharField(max_length=100)
    pack = models.CharField(max_length=50)
    expiry = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    where_production = models.CharField(max_length=50)
    dosage_form = models.CharField(max_length=50)
    description = RichTextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_medicine}"

    @property
    def discount_percentage(self):
        try:
            offer_product = self.category_offers
            return offer_product.discount
        except OfferProduct.DoesNotExist:
            return 0

    def to_dict(self):
        serialized_obj = serialize('python', [self,])
        fields = serialized_obj[0]['fields']
    
        fields['category'] = {
            'id': self.category.id,
            'name': self.category.name,
            'parent': self.category.parent_id,
            'image': self.category.image
        }
        fields['unit'] = {
            'id': self.unit.id,
            'name': self.unit.name
        }
        fields['name_medicine'] = self.name_medicine
        return fields


class OfferProduct(models.Model):
    medicine = models.OneToOneField(Medicine, related_name='category_offers', on_delete=models.CASCADE)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], null=True, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.medicine.name_medicine


class Payment(models.Model):
    id_payment = models.AutoField(primary_key=True)
    pay_method = models.CharField(max_length=50)

    def __str__(self):
        return self.pay_method


class Cart(models.Model):
    id_cart = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class DetailCart(models.Model):
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    id_payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]
    id_order = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10, default='null')
    receiver = models.CharField(max_length=50, default='null')
    status_id = models.CharField(max_length=50, choices=STATUS_CHOICES)
    total_price = models.IntegerField(default=0, editable=False)
    created = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)


