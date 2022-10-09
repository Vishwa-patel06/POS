from django.db import models
from Static_Master.models import *
from Universal.models import *
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.

class CustomerModel(models.Model):
    userObject = models.ForeignKey(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)

    # Company Details
    gstNumber = models.CharField(max_length=255, null=True, blank=True)

    # Contact Details
    # contactPersonName = models.CharField(max_length=255)
    contactNumber = models.CharField(max_length=255, null=True, blank=True, unique=True)
    contactEmail = models.CharField(max_length=255, null=True, blank=True, unique=True)
    customerWebsite = models.CharField(max_length=255, null=True, blank=True)

    # Address
    address = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE, null=True, blank=True)
    district = ChainedForeignKey(DistrictModel, chained_field="state", chained_model_field="stateObject",
                      show_all=False, auto_choose=True, sort=True, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName)

    class Meta:
        verbose_name = "    Customer List"
        verbose_name_plural = "    Customer List"

class CustomerBankModel(models.Model):
    customerObject = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    BankObject = models.ForeignKey(BankModel, on_delete=models.CASCADE)
    accountNumber = models.CharField(max_length=255)
    ifsc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.customerObject, self.BankObject)

    class Meta:
        verbose_name = "  Bank List"
        verbose_name_plural = "  Bank List"

# class CustomerShipmentModel(models.Model):
#     customerObject = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
#     firmName = models.CharField(max_length=255)
#     gstNumber = models.CharField(max_length=255, null=True, blank=True)
#     panNumber = models.CharField(max_length=255, null=True, blank=True)
#
#     # Contact Details
#     contactPersonName = models.CharField(max_length=255)
#     contactNumber = models.CharField(max_length=255, null=True, blank=True)
#     contactEmail = models.CharField(max_length=255, null=True, blank=True)
#     customerWebsite = models.CharField(max_length=255, null=True, blank=True)
#
#     # Address
#     address = models.TextField(null=True, blank=True)
#     pincode = models.CharField(max_length=255, null=True, blank=True)
#     town = models.CharField(max_length=255, null=True, blank=True)
#     state = models.ForeignKey(StateModel, on_delete=models.CASCADE, null=True, blank=True)
#     district = ChainedForeignKey(DistrictModel, chained_field="state", chained_model_field="stateObject",
#                                  show_all=False, auto_choose=True, sort=True, null=True, blank=True)
#
#     def __str__(self):
#         return '{} ({})'.format(self.firmName, self.customerObject)
#
#     class Meta:
#         verbose_name = "  Customer Shipment List"
#         verbose_name_plural = "   Customer Shipment List"





