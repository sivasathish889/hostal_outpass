
from django.db import models
from django.utils.timezone import localtime

# Create your models here.
class RegisterModel(models.Model):

    class yearChoice(models.IntegerChoices):
        1, "First Year",
        2, "Second Year",
        3, "Third Year",
        4, "Final Year",
    
    MONTH_CHOICES = (
    (1, "First Year"),
    (2, "Second year"),
    (3, "Third year"),
    (4, "Final year"),
    )
    id = models.BigAutoField(blank=False, primary_key=True)
    name = models.CharField(max_length=150, blank=False, null=False)
    register_number = models.CharField(unique=True, blank=False, null=False, max_length=255)
    department = models.CharField(max_length=150, blank=False, null=False )
    district = models.CharField(max_length=100,blank=False, null=False)
    phone_number = models.BigIntegerField(blank=False, null=False)
    parent_number= models.BigIntegerField(blank=False, null=True)
    year = models.CharField(blank=False, null=True, choices=MONTH_CHOICES, help_text='1-first_year, 2-second_year, 3-third_year, 4-final_year', max_length=150)
    email = models.EmailField( max_length=254,blank=False, null=False)
    password = models.CharField(max_length=200,blank=False, null=False)
    created_at = models.DateField( auto_now_add=True, blank=False,null=False)
    updated_at = models.DateField(auto_now=True, blank=False,null=False)

    def __str__(self):
        return self.name
    
class RequestModel(models.Model):
    actionChoice= ( (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Rejected'))

    user = models.BigIntegerField(blank=False,null=False)
    regNo = models.BigIntegerField(blank=False,null=False)
    phone_number = models.BigIntegerField(blank=False,null=False)
    name = models.CharField(blank=False,null=False, max_length=150)
    purpose = models.CharField( max_length=150,blank=False, null=False)
    inTime = models.DateTimeField( blank=False,null=False)
    outTime = models.DateTimeField(blank=False,null=False)
    pending = models.CharField(choices = actionChoice,default=1, blank=False, null=True, help_text='1-pending, 2-accepted, 3-rejected',max_length=100)
    actionWarden = models.CharField(null=True, blank=False, max_length=50)
    gateInTime = models.DateTimeField( blank=True, null=True)
    gateOutTime = models.DateTimeField( blank=True, null=True)
    outpassEnd = models.BooleanField(blank=False, null=False, default=0)
    roomNo = models.CharField(blank=False,null=True,max_length=100)
    
    def __str__(self):
        return self.name
    
    @property
    def localInTime(self):
        return  localtime(self.inTime)
    @property
    def localOutTime(self):
        return localtime(self.outTime)