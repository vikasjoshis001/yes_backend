from rest_framework import serializers

from .models import TransactionHistoryModel

# Transaction History Serializer


class TransactionHistorySerializer(serializers.ModelSerializer):
    """ Transaction History Model Serializer """
    class Meta:
        model = TransactionHistoryModel
        fields = "__all__"
