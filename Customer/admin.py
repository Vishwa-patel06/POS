from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import *
from django.contrib.admin import TabularInline
# Register your models here.

# Register your models here.

class CustomerBankInline(TabularInline):
    extra = 0
    model = CustomerBankModel

class CustomerAdmin(ImportExportMixin, admin.ModelAdmin):
    inlines = [CustomerBankInline]
    list_display = ['firstName', 'lastName', 'district', 'pincode']

admin.site.register(CustomerModel, CustomerAdmin)
