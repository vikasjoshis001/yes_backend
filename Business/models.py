from django.db import models

# Create your models here.


# Business Model
class BusinessModel(models.Model):
    """ Business Database Table """
    businessId = models.AutoField(primary_key=True)
    businessName = models.CharField(max_length=200)
    businessCreatedAt = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    businessUpdatedAt = models.DateTimeField(
        auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.businessName
