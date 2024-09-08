from django.urls import path
from warden.views import *

urlpatterns = [
    path("login/", loginPage, name='wardenloginpage'),
    path('', index, name='indexpage')
]
