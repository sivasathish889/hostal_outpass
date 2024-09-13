from django.shortcuts import render,redirect
from student.models import *
from django.contrib.auth.hashers import make_password,check_password
from django.core import serializers
import json
from django.contrib import messages
import jwt


def loginPage(request):
    if request.method == 'POST':
        registerNumber = request.POST['register_number']
        password = request.POST['password']
        regNo = RegisterModel.objects.filter(register_number=registerNumber)
        if not regNo:
            messages.warning(request,message="You are not register..Please register")
            return redirect('studentloginpage')
        else:
            user = serializers.serialize('json', regNo)
            data = json.loads(user)
            db_pass = data[0]['fields']['password']
            hashpass = check_password(password, db_pass)
            if hashpass:
                messages.success(request, "Login Successfully")
                res =  redirect("index")
                token = jwt.encode(payload=data[0],algorithm="HS256",key="secretKey")
                res.set_cookie('user', token)
                return res
            else:
                messages.warning(request ,message='Password Incorrect')
                return redirect('studentloginpage')

    return render(request, "student/loginPage.html")

def RegisterPage(request):  
    if request.method == 'POST':
        name = request.POST['username']
        register_number = request.POST['register_number']
        department = request.POST['department']
        district = request.POST['district']
        phone_number = request.POST['phone_number']
        parent_number = request.POST['parent_number']
        year = request.POST['year']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if not RegisterModel.objects.filter(register_number = register_number).exists():
            if pass1 == pass2:
                password = make_password(pass1)
                user = RegisterModel.objects.create(
                    name =name.upper(),
                    register_number = register_number,
                    department = department.upper(),
                    district = district.upper(),
                    phone_number = phone_number,
                    parent_number = parent_number,
                    email = email,
                    year = year,
                    password = password)
                user.save()
                messages.success(request, message='Register Successfully')
                return redirect('studentloginpage')
            else:
                messages.warning(request,message="password Mismatched")
                return render(request, "student/registerPage.html", context={"messages" : "password mismated", "tags" : "danger"})
        else:
            messages.warning(request, message="User is already Registered")
            return redirect('studentloginpage')
    
    return render(request, "student/registerPage.html")

def logOut(request):
    messages.success(request, message='Logout Successfully')
    res =  render(request,'student/loginpage.html')
    res.delete_cookie('user')
    return res


def indexPage(request):
    if "user" in request.COOKIES.keys():
        cookie = request.COOKIES['user']
        decodeData = jwt.decode(cookie, key="secretKey", algorithms="HS256")
        regNo = decodeData['fields']['register_number']
        user = RegisterModel.objects.filter(register_number = regNo)
        user = serializers.serialize('json', user)
        data = json.loads(user)
        db_pass = data[0]['fields'] 
        if db_pass['year'] == 1:
            years = 'First Year'
        elif db_pass['year'] == 2:
            years = 'Second Year'
        elif db_pass['year'] == 3:
            years = 'Third Year'
        else:
            years = 'Final Year'
            
        datas = RequestModel.objects.filter(regNo = regNo,pending = 1).order_by('inTime').reverse()
        users = serializers.serialize('json', datas)
        dataa= json.loads(users)
        return render(request, "student/index.html", context={
            "name" : db_pass['name'],
            'regNo' : db_pass['register_number'],
            'pNumber' : db_pass['phone_number'],
            'year' : years,
            'parent_number' : db_pass['parent_number'],
            "data" : dataa
        })
    return redirect('studentloginpage')


def request(request):
    
    if request.method == 'POST':
        regNo = request.POST['regNo']
        phone_number = request.POST['phone_number']
        name = request.POST['username']
        purpose = request.POST['purpose']
        inTime = request.POST['inTime']
        outTime = request.POST['outTime']
        roomNo = request.POST['roomNo']
        user = RegisterModel.objects.filter(register_number = regNo)
        user = serializers.serialize('json', user)
        data = json.loads(user)
        db_pass = data[0]['pk']
        req = RequestModel.objects.create(
            user = db_pass,
            regNo = regNo,
            phone_number = phone_number,
            name = name,
            purpose = purpose,
            inTime = inTime,
            outTime = outTime,
            roomNo = roomNo
        )
        req.save()
        messages.success(request, message='Request send')
        return redirect('index')
            
    return render(request, 'student/request.html')

def preRequest(request):
    cookie = request.COOKIES['user']
    decodeData = jwt.decode(cookie, key="secretKey", algorithms="HS256")
    regNo = decodeData['fields']['register_number']
    datas = RequestModel.objects.filter(regNo = regNo,pending__in = [2,3]).order_by('inTime').reverse()
    print(datas)
    users = serializers.serialize('json', datas)
    dataa= json.loads(users)
    return render(request, 'student/preRequest.html', context={'reqData' : dataa})