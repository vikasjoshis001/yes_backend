from django.contrib import admin
from .models import CustomersModel, TransactionHistoryModel
# Register your models here.

admin.site.register(CustomersModel)
admin.site.register(TransactionHistoryModel)
