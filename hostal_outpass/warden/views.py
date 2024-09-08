from django.shortcuts import render,redirect
from warden.models import *
from student.models import *
from django.contrib import messages
from django.core.serializers import serialize
from django.contrib.auth import logout
import json
# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = WardenRegisterModel.objects.filter(username=username, password = password)
        serializing = serialize('json', user)
        data = json.loads(serializing)
        pk = data[0]['pk']
        print(pk)
        if len(user) != 0:
            messages.success(request, message='Login Successfully')
            res = redirect('indexpage')
            res.set_cookie('warden',pk)
            return res
        else:
            messages.warning(request,message = "User Not Found")
            return render(request, 'warden/loginPage.html')
    return render(request, "warden/loginPage.html")

def index(request):
    if 'warden' in request.COOKIES.keys():
        req = RequestModel.objects.filter(pending = 1)
        serializing = serialize('json', req)
        data = json.loads(serializing)
        return render(request, 'warden/index.html', context={'data' : data})
    else:
        messages.warning(request, message='Please Login')
        return redirect('wardenloginpage')


def logOut(request):
    logout(request)
    res = redirect('wardenloginpage')
    res.delete_cookie('warden')
    return res


def wardenAccept(request,id):
    RequestModel.objects.filter(pk=id).update(pending = 2)
    messages.success(request, message='Accpeted')
    return redirect('indexpage')

def wardenReject(request, id):
    RequestModel.objects.filter(pk=id).update(pending = 3)
    messages.success(request, message='Rejected')
    return redirect('indexpage')