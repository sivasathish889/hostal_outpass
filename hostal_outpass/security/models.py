from django.db import models

# Create your models here.

class securityLoginModel(models.Model):
    username = models.CharField(blank=False, null=False, max_length=500)
    password = models.CharField(blank=False, null=False, max_length=500)
    phone_number = models.BigIntegerField(verbose_name="security_phone_number", null=True, blank=True)

    def __str__(self) :
        return self.username