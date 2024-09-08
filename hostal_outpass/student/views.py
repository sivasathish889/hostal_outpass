from django.shortcuts import render,redirect
from student.models import *
from django.contrib.auth.hashers import make_password,check_password
from django.core import serializers
import json


def loginPage(request):
    if request.method == 'POST':
        registerNumber = request.POST['register_number']
        password = request.POST['password']
        regNo = RegisterModel.objects.filter(register_number=registerNumber)
        if not regNo:
            print("You are not register..Please register")
            return render(request, "student/loginPage.html", context={"messages" : "You are not register..Please register", "tags" : "warning"})
        else:
            user = serializers.serialize('json', regNo)
            data = json.loads(user)
            db_pass = data[0]['fields']['password']
            hashpass = check_password(password, db_pass)
            if hashpass:
                print("ok")
                res =  redirect("index")
                res.set_cookie('user', registerNumber)
                return res
            else:
                print("password incorrect")

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
                password = make_password(pass1,)
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
                return redirect('loginpage')
            else:
                print("password Mismatched")
                return render(request, "student/registerPage.html", context={"messages" : "password mismated", "tags" : "danger"})
        else:
            print("User is already Registered")
    
    return render(request, "student/registerPage.html")

def logOut(request):
    res =  render(request,'student/loginpage.html')
    res.delete_cookie('user')
    return res


def indexPage(request):
    if "user" in request.COOKIES.keys():
        regNo = request.COOKIES['user']
        user = RegisterModel.objects.filter(register_number = regNo)
        user = serializers.serialize('json', user)
        data = json.loads(user)
        db_pass = data[0]['fields'] 
        
        if db_pass['year']==1:
            years = 'First Year'
        elif db_pass['year'] == 2:
            years = 'Second Year'
        elif db_pass['year'] == 3:
            years = 'Third Year'
        else:
            years = 'Final Year'
        datas = RequestModel.objects.filter(regNo = regNo)
        users = serializers.serialize('json', datas)
        dataa= json.loads(users)
        print(dataa)
        return render(request, "student/index.html", context={
            "name" : db_pass['name'],
            'regNo' : db_pass['register_number'],
            'pNumber' : db_pass['phone_number'],
            'year' : years,
            'parent_number' : db_pass['parent_number'],
            "data" : dataa
        })
    return redirect('loginpage')


def request(request):
    
    if request.method == 'POST':
        regNo = request.POST['regNo']
        phone_number = request.POST['phone_number']
        name = request.POST['username']
        purpose = request.POST['purpose']
        inTime = request.POST['inTime']
        outTime = request.POST['outTime']
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
            outTime = outTime
        )
        req.save()
        return redirect('index')
        
    return render(request, 'student/request.html')