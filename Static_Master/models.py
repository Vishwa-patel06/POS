from django.db import models

# Create your models here.

class StateModel(models.Model):
    stateName = models.CharField(max_length=255)

    def __str__(self):
        return self.stateName

    class Meta:
        verbose_name = "    State List"
        verbose_name_plural = "    State List"

class DistrictModel(models.Model):
    stateObject = models.ForeignKey(StateModel, on_delete=models.CASCADE)
    districtName = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.districtName, self.stateObject)

    class Meta:
        verbose_name = "    District List"
        verbose_name_plural = "    District List"

# class PermissionsModel(models.Model):
#     title = models.CharField(max_length=255)
#     code = models.CharField(max_length=255)
#     description = models.TextField()
#
#     def __str__(self):
#         return '{} - {}'.format(self.code, self.title)
#
#     class Meta:
#         verbose_name = " Permission List"
#         verbose_name_plural = " Permission List"


class BankModel(models.Model):
    bankName = models.CharField(max_length=255)

    def __str__(self):
        return self.bankName

    class Meta:
        verbose_name = " Bank List"
        verbose_name_plural = " Bank List"