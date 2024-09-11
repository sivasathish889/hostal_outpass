from django.shortcuts import render, redirect
from security.models import *
from django.contrib import messages
from student.models import RequestModel
from django.core.serializers import serialize
import json
import datetime
import jwt
# Create your views here.

def securityIndex(request):
    if 'security' in request.COOKIES.keys():
        cookie = request.COOKIES['security']
        decodeData = jwt.decode(cookie, key="secretKey", algorithms="HS256")
        username = decodeData['fields']['username']
        password = decodeData['fields']['password']
        user = securityLoginModel.objects.filter(username= username, password= password)
        if len(user) != 0:
            req = RequestModel.objects.filter(pending = 2,outpassEnd=0)
            serializing = serialize('json', req)
            data = json.loads(serializing)
            return render(request, "security/index.html", context={"data" : data})
        else:
            messages.warning(request, message="You are unAuthorized Person")
            return redirect('securityindexpage')
    messages.warning(request, message="Please Login")
    return render(request, "security/securityLoginPage.html")

def securiryLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = securityLoginModel.objects.filter(username= username, password = password)
        serializing = serialize('json', user)
        data = json.loads(serializing)
        if len(user) != 0:
            res = redirect('securityindexpage')
            encodeData = jwt.encode(payload=data[0],key="secretKey", algorithm="HS256")
            res.set_cookie('security', encodeData)
            messages.success(request, message="Login Successful")
            return res
        else:
            messages.warning(request, message="You are Unauthorized Person")
            return redirect('securityloginpage')
    return render(request, "security/securityLoginPage.html")

current_datetime = datetime.datetime.now()
datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

def inTimeRegister(request,id):
    RequestModel.objects.filter(pk = id).update(gateInTime = datetime_string,outpassEnd=1)
    messages.success(request, message="Outpass Ended")
    return redirect( "securityindexpage")


def outTimeRegister(request,id):
    RequestModel.objects.filter(pk = id).update(gateOutTime = datetime_string)
    messages.success(request, message="In Time Register")
    return redirect( "securityindexpage")

def logOut(request):
    res = redirect('securityloginpage')
    res.delete_cookie('security')
    messages.success(request, message="Logout Successfully")
    return res