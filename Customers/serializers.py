from rest_framework import serializers

from .models import CustomersModel, TransactionHistoryModel

# Customer Serializer


class CustomersSerializer(serializers.ModelSerializer):
    """ Customers Model Serializer """
    class Meta:
        model = CustomersModel
        fields = "__all__"

# Transaction History Serializer


class TransactionHistorySerializer(serializers.ModelSerializer):
    """ Transaction History Model Serializer """
    class Meta:
        model = TransactionHistoryModel
        fields = "__all__"
