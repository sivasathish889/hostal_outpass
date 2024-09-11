from django.shortcuts import render,redirect
from warden.models import *
from student.models import *
from django.contrib import messages
from django.core.serializers import serialize
from django.contrib.auth import logout
import json
import jwt

# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = WardenRegisterModel.objects.filter(username=username, password = password)
        serializing = serialize('json', user)
        data = json.loads(serializing)
        if len(user) != 0:
            messages.success(request, message='Login Successfully')
            res = redirect('indexpage')
            encodeData = jwt.encode(payload=data[0], algorithm="HS256", key="secretKey")
            res.set_cookie('warden',encodeData)
            return res
        else:
            messages.warning(request,message = "User Not Found")
            return render(request, 'warden/loginPage.html')
    return render(request, "warden/loginPage.html")

def index(request):
    if 'warden' in request.COOKIES.keys():
        cookie = request.COOKIES['warden']
        decodeData = jwt.decode(cookie, key="secretKey", algorithms="HS256")
        username = decodeData['fields']['username']
        password = decodeData['fields']['password']
        user = WardenRegisterModel.objects.filter(username=username, password = password)
        serializing = serialize('json', user)
        data = json.loads(serializing)
        if len(user) != 0:
            req = RequestModel.objects.filter(pending = 1)
            print(req)
            serializing = serialize('json', req)
            data = json.loads(serializing)
            return render(request, 'warden/index.html', context={'data' : data})
        else:
            messages.warning(request, message='Unauthorized User')
            return redirect("wardenloginpage")
    messages.warning(request, message='Please Login')
    return render(request, "warden/loginPage.html")


def logOut(request):
    logout(request)
    res = redirect('wardenloginpage')
    res.delete_cookie('warden')
    return res


def wardenAccept(request,id):
    cookie = request.COOKIES['warden']
    decodeData = jwt.decode(cookie, key="secretKey", algorithms="HS256")
    RequestModel.objects.filter(pk=id).update(pending = 2,actionWarden =decodeData['fields']['username'])
    messages.success(request, message='Accpeted')
    return redirect('indexpage')

def wardenReject(request, id):
    RequestModel.objects.filter(pk=id).update(pending = 3 )
    messages.success(request, message='Rejected')
    return redirect('indexpage')