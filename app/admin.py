from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    CustomerPayment, Payment, CoverGenerator, HomePage, Profile,
    PaymentFeature, FAQ
)
from core.models import CustomUser

# Register your models here.
class PaymentFeatureAdmin(admin.TabularInline):
    model = PaymentFeature

class PaymentAdmin(admin.TabularInline):
    model = Payment

class PaymentFeatureAdmin(admin.ModelAdmin):
   inlines = [PaymentAdmin,]

class HomePageAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_cover_img', 'cover_num']

admin.site.register(Payment)
admin.site.register(CustomerPayment)
admin.site.register(CoverGenerator)
admin.site.register(CustomUser)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(Profile)
admin.site.register(PaymentFeature, PaymentFeatureAdmin)
admin.site.register(FAQ)
