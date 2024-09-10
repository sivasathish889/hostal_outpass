
from django.urls import path
from security.views import *
urlpatterns = [
    path('login/', wardenLogin, name='securityloginpage'),  
    path('',securityIndex, name='securityindexpage'),
    path('<str:id>/', inTimeRegister, name="intimeregister"),
    path('<str:id>/', outTimeRegister, name="outtimeregister")
]
