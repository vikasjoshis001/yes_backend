from rest_framework import serializers

from .models import CustomersModel,SavePdf,YesMultiServicesLogo

# Customer Serializer


class CustomersSerializer(serializers.ModelSerializer):
    """ Customers Model Serializer """
    class Meta:
        model = CustomersModel
        fields = "__all__"
        
class SavePdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavePdf
        fields = '__all__'
        
class YesMultiServicesLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YesMultiServicesLogo
        fields = '__all__'
