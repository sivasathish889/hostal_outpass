from django.urls import path
from student.views import *


urlpatterns = [
    path("", indexPage, name="index"),
    path("student/register/", RegisterPage, name="registerpage"),
    path("student/login/", loginPage, name='studentloginpage'),
    path("student/Request", request, name='Request'),
    path('student/logout', logOut, name='studentlogout'),
    path('student/preRequest/', preRequest, name='preRequest'),
    path('student/forget-password',forget_password, name='forgetpassword'),
    path('student/confirm-otp', confirm_OTP, name='confirmOTP')

]
