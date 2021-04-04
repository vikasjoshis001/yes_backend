from django.db import models
from Customers.models import CustomersModel
from Business.models import BusinessModel
# Create your models here.

# Transaction History Model


class TransactionHistoryModel(models.Model):
    """ Transaction History Database Table """
    transactionId = models.AutoField(primary_key=True)
    transactionName = models.CharField(max_length=200)
    transactionCredit = models.CharField(max_length=200)
    transactionDebit = models.CharField(max_length=20)
    transactionPending = models.CharField(max_length=200)
    transactionCustomer = models.ForeignKey(
        CustomersModel, on_delete=models.CASCADE)
    transactionBusiness = models.ForeignKey(
        BusinessModel, on_delete=models.CASCADE)
    transactionDate = models.DateField(auto_now_add=True)
    transactionTime = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.transactionName
