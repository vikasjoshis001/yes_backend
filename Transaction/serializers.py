from rest_framework import serializers, fields

from .models import TransactionHistoryModel

# Transaction History Serializer


class TransactionHistorySerializer(serializers.ModelSerializer):
    """ Transaction History Model Serializer """
    
    transactionTime = fields.TimeField(input_formats=['%H %M %S'])
    
    class Meta:
        model = TransactionHistoryModel
        fields = "__all__"
