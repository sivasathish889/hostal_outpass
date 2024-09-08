from django.contrib import admin
from warden.models import *
class RegisterModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'phone_number']
# Register your models here.
admin.site.register(WardenRegisterModel,RegisterModelAdmin)