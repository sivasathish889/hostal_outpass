from django.urls import path
from warden.views import *

urlpatterns = [
    path("login/", loginPage, name='wardenloginpage'),
    path('', index, name='indexpage'),
    path('logout', logOut, name='logout'),
    path('accept/<str:id>', wardenAccept, name='wardenAccept'),
    path('reject/<str:id>', wardenReject, name='wardenReject'),
]
