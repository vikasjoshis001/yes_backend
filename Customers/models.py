from Business.models import BusinessModel
from django.db import models

# Create your models here.

# Customer Model


class CustomersModel(models.Model):
    """ Customer Database Table """
    customerId = models.AutoField(primary_key=True)
    customerName = models.CharField(max_length=200)
    customerCredit = models.CharField(max_length=20)
    customerDebit = models.CharField(max_length=20)
    customerPending = models.CharField(max_length=20)
    customerContact = models.CharField(max_length=10,blank=True,null=True)
    customerAddress = models.TextField(max_length=500,blank=True,null=True)
    customerAadharNumber = models.CharField(max_length=12,blank=True,null=True)
    customerPanNumber = models.CharField(max_length=10,blank=True,null=True)
    customerBusiness = models.ForeignKey(
        BusinessModel, on_delete=models.CASCADE)
    creationTime = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )

    def __str__(self):
        return self.customerName

# Transaction History Model


class TransactionHistoryModel(models.Model):
    """ Transaction History Database Table """
    transactionId = models.AutoField(primary_key=True)
    transactionName = models.CharField(max_length=200)
    transactionCredit = models.CharField(max_length=200)
    transactionDebit = models.CharField(max_length=200)
    transactionPending = models.CharField(max_length=200)
    transactionContact = models.CharField(max_length=200,blank=True,null=True)
    transactionAddress = models.TextField(max_length=500,blank=True,null=True)
    transactionAadharNumber = models.CharField(max_length=12,blank=True,null=True)
    transactionPanNumber = models.CharField(max_length=10,blank=True,null=True)
    transactionCustomer = models.ForeignKey(
        CustomersModel, on_delete=models.CASCADE)
    transactionBusiness = models.ForeignKey(
        BusinessModel, on_delete=models.CASCADE)
    creationTime = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )

    def __str__(self):
        return self.transactionName
