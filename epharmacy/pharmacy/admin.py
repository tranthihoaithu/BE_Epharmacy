import os

from django.contrib import admin
from django import forms
from django.contrib.auth.models import Permission


from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MedicienForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Medicine
        fields = '__all__'


class MedicienAdmin(admin.ModelAdmin):
    form = MedicienForm
    list_display = ['id_medicine', 'name_medicine', 'stock_quantity', 'price', 'discount_price', 'active']
    # list_filter = ['name_medicine', 'category']
    search_fields = ['id_medicine', 'name_medicine']
    # readonly_fields = ['avatar']
    #
    # def avatar(self, Medicien):
    #     return mark_safe("<img src='/static/{img_url}' alt='{alt}' />".format(img_url=Medicien.image.name, alt=Medicien.subject))
    #

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status_id']


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ['id_order', 'user_id', 'total_price', 'shipping_address', 'phone_number', 'receiver', 'status_id']
    list_editable = ['status_id']


class OfferProductForm(forms.ModelForm):
    class Meta:
        model = OfferProduct
        fields = '__all__'


class OfferProductAdmin(admin.ModelAdmin):
    form = OfferProductForm
    list_display = ['medicine', 'discount']

    def save_model(self, request, obj, form, change):
        # Gọi phương thức save_model mặc định của lớp cha
        super().save_model(request, obj, form, change)
        if obj.discount is not None:
            obj.medicine.discount_price = obj.medicine.price - (obj.medicine.price * obj.discount / 100)
        else:
            obj.medicine.discount_price = obj.medicine.price
        obj.medicine.save()

    def delete_queryset(self, request, queryset):
        # Lặp qua từng đối tượng được chọn để xóa
        for obj in queryset:
            obj.delete()
            if obj.discount is not None:
                obj.medicine.discount_price = None
            else:
                obj.medicine.discount_price = obj.medicine.price
            obj.medicine.save()


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

class PharmacyAppAdminSite(admin.AdminSite):
    site_header = "Hệ Thống Bán Thuốc Trực Tuyến"


admin_site = PharmacyAppAdminSite(name=' mypharmacy ')


admin_site.register(Category)
admin_site.register(Medicine, MedicienAdmin)
admin_site.register(Unit)
admin_site.register(User, UserProfileAdmin)
admin_site.register(Permission)
admin_site.register(Payment)
admin_site.register(Order, OrderAdmin)
admin_site.register(OfferProduct, OfferProductAdmin)


