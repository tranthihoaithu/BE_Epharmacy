from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from ckeditor.fields import RichTextField
from django.core.serializers import serialize
import json


class User(AbstractUser):
    avatar = models.ImageField(upload_to='upload/%y/%m/%d/', blank=True)

#
# class CreateUser(AbstractUser):
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, null=False)

    def __str__(self):
        return self.name


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
    source = models.CharField(max_length=100)
    stock_quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    ingredient = models.CharField(max_length=100)
    content = RichTextField()
    uses = models.CharField(max_length=100)
    side_effects = models.CharField(max_length=100)
    object = models.CharField(max_length=100)
    pack = models.CharField(max_length=50)
    expiry = models.CharField(max_length=50)
    product_type = models.CharField(max_length=50)
    description = RichTextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_medicine}"
    
    def to_dict(self):
        serialized_obj = serialize('python', [self,])
        fields = serialized_obj[0]['fields']
    
        fields['category'] = {
            'id': self.category.id,
            'name': self.category.name
        }
        fields['name_medicine'] = self.name_medicine

        return fields


class Invoice(models.Model):
    id_invoice = models.AutoField(primary_key=True)
    created_day = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


class DetailInvoice(models.Model):
    id_detail_invoice = models.AutoField(primary_key=True)
    id_invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    id_medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, unique=True)


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
    id_order = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)











# class Category(models.Model):
#     name = models.CharField(max_length=100, null=False, unique=True)
#
#     def __str__(self):
#         return self.name


# class ItemBase(models.Model):
#     class Meta:
#         abstract = True
#
#     subject = models.CharField(max_length=100, null=False)
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)
#     image = models.ImageField(upload_to='pharmacy/%y/%m', default=None)
#
#     def __str__(self):
#         return self.subject
#
#
# class Course(ItemBase):
#     class Meta:
#         unique_together = ('subject', 'category')
#         ordering = ["-id"]  # sap xep giam dan
#
#     description = models.TextField(null=True, blank=True)
#
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)  # khóa ngoại của Category, ondelete là khi category xoóa đi thì trường này sẽ nh thế nào
#
#
# class Lesson(ItemBase):
#     class Meta:
#         unique_together = ('subject', 'course')
#         # db_table = 'lesson' : đặt tên table
#
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
#     tags = models.ManyToManyField('Tag', blank=True, null=True)
#
#
# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name
