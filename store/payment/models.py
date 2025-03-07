from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True , blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True , blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255 , null=True , blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True , blank=True)
    shipping_country = models.CharField(max_length=255)

    # dont pluralize address
    class Meta:
        verbose_name_plural = "shipping address"

    def __str__(self):
        return f'shipping address - {str(self.id)}'




