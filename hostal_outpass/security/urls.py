
from django.urls import path
from security.views import *
urlpatterns = [
    path('login/', securiryLogin, name='securityloginpage'),  
    path('',securityIndex, name='securityindexpage'),
    path('inTimeRegister/<str:id>/', inTimeRegister, name="intimeregister"),
    path('outTimeRegister/<str:id>/', outTimeRegister, name="outtimeregister"),
    path("logout/", logOut, name="securitylogout")
]
