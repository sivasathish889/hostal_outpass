from django.contrib import admin
from student.models import *

class registerModelAdmin(admin.ModelAdmin):
    list_display = [ "name", "register_number", "department", "phone_number" ]

    
# Register your models here.
admin.site.register(RegisterModel,registerModelAdmin)