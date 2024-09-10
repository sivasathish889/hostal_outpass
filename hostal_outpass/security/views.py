from django.shortcuts import render, redirect
from security.models import *
from django.contrib import messages
from student.models import RequestModel
from django.core.serializers import serialize
import json
import datetime
import pytz
# Create your views here.

def securityIndex(request):
    if 'security' in request.COOKIES.keys():
        req = RequestModel.objects.filter(pending = 2)
        serializing = serialize('json', req)
        data = json.loads(serializing)
        return render(request, "security/index.html", context={"data" : data})
    else:
        messages.warning(request, message="Please Login")
        return render(request, "security/securityLoginPage.html")

def wardenLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if len(securityLogin.objects.filter(username= username, password = password)) != 0:
            res = redirect('securityindexpage')
            res.set_cookie('security', username)
            return res
        else:
            messages.warning(request, message="You are Unauthorized Person")
            return redirect('securityloginpage')
    return render(request, "security/securityLoginPage.html")

current_datetime = datetime.datetime.now()
datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

def inTimeRegister(request,id):
    RequestModel.objects.filter(pk = id).update(gateInTime = datetime_string)

    return redirect( "securityindexpage")


def outTimeRegister(request,id):
    RequestModel.objects.filter(pk = id).update(gateOutTime = datetime_string)
    return redirect( "securityindexpage")