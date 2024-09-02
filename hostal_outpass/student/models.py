from django.db import models

# Create your models here.
class RegisterModel(models.Model):
    name = models.CharField(max_length=150)
    register_number = models.BigIntegerField(unique=True,primary_key=True)
    department = models.CharField(max_length=150, default='')
    district = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    email = models.EmailField( max_length=254)
    password = models.CharField(max_length=200)

    
    