from django.db import models

# Create your models here.
class WardenRegisterModel(models.Model):
    username = models.CharField( max_length=150, unique=True, blank=False, null=False)
    password = models.CharField( max_length=150, blank=False, null=False)
    phone_number = models.BigIntegerField(blank=False, null=False)
