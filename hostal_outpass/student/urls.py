from django.urls import path
from student.views import *
urlpatterns = [
    path("student/", indexPage, name="index"),
    path("student/register/", RegisterPage, name="registerpage"),
    path("student/login/", loginPage, name='loginpage'),
    path("student/Request", request, name='Request'),
    path('logout', logOut, name='logout')
]
