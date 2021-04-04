from Business.models import BusinessModel
from django.db import models

# Create your models here.

# Customer Model


class CustomersModel(models.Model):
    """ Customer Database Table """
    customerId = models.AutoField(primary_key=True)
    customerName = models.CharField(max_length=200)
    customerContact = models.CharField(max_length=10, blank=True, null=True)
    customerAddress = models.TextField(max_length=500, blank=True, null=True)
    customerAadharNumber = models.CharField(
        max_length=12, blank=True, null=True)
    customerPanNumber = models.CharField(max_length=10, blank=True, null=True)
    customerDOB = models.CharField(max_length=20, blank=True, null=True)
    customerCredit = models.CharField(max_length=20,blank=True, null=True,default=0)
    customerDebit = models.CharField(max_length=20,blank=True, null=True,default=0)
    customerPending = models.CharField(max_length=20,blank=True, null=True)
    customerStatus = models.BooleanField(default=False)
    customerBusiness = models.ForeignKey(
        BusinessModel, on_delete=models.CASCADE)
    creationTime = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )

    def __str__(self):
        return self.customerName
