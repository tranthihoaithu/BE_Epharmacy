from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
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
    list_display = ['id_medicine', 'name_medicine', 'content', 'stock_quantity', 'price', 'active']
    list_filter = ['name_medicine', 'category']
    search_fields = ['id_medicine', 'name_medicine']
    readonly_fields = ['avatar']

    def avatar(self, Medicien):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' />".format(img_url=Medicien.image.name, alt=Medicien.subject))






# class LessonTagInline(admin.TabularInline):
#     model = Lesson.tags.through


# class LessonAdmin(admin.ModelAdmin):
#     class Media:
#         css = {
#             'all': ('/static/css/main.css', )
#         }
#
#     form = LessonForm
#     list_display = ["id", "subject", "created_date", "active", "course"]
#     search_fields = ["subject", "created_date"]
#     list_filter = ["subject", "course__subject"]
#     readonly_fields = ["ava"]
#     inlines = [LessonTagInline, ]
#
#     def ava(self, lesson):
#         return mark_safe("<img src='/static/{img_url}' alt='{alt}' width='120px' />".format(img_url=lesson.image.name, alt=lesson.subject))
#
#
# class LessonInline(admin.StackedInline):
#     model = Lesson
#     pk_name = 'course'
#
#
# class CourseAdmin(admin.ModelAdmin):
#     inlines = (LessonInline, )
#
#
class PharmacyAppAdminSite(admin.AdminSite):
    site_header = "Hệ Thống Bán Thuốc Trực Tiếp"


admin_site = PharmacyAppAdminSite(name=' mypharmacy ')

# admin_site.register(Category)
# admin_site.register(Course, )
# admin_site.register(Medicine, MedicienAdmin)

# admin.site.register(CreateUser)

admin_site.register(Category)
admin_site.register(Medicine, MedicienAdmin)
admin_site.register(Cart)
admin_site.register(Unit)
admin_site.register(User)
admin_site.register(Permission)
admin_site.register(Payment)

# admin.site.register(Category)
# admin.site.register(Medicine, MedicienAdmin)
# admin.site.register(Cart)
# admin.site.register(Unit)
