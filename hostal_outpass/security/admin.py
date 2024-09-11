from django.contrib import admin
from security.models import *
# Register your models here.
class secrityLoginAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number']

admin.site.register(securityLoginModel,secrityLoginAdmin)