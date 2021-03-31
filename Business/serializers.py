from rest_framework import serializers


from .models import BusinessModel

# Business Model Serializer


class BusinessSerializer(serializers.ModelSerializer):
    """ Business Model Serializer """
    class Meta:
        model = BusinessModel
        fields = "__all__"
