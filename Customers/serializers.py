from rest_framework import serializers

from .models import CustomersModel

# Customer Serializer


class CustomersSerializer(serializers.ModelSerializer):
    """ Customers Model Serializer """
    class Meta:
        model = CustomersModel
        fields = "__all__"
