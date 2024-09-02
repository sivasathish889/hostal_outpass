from django.shortcuts import render,redirect
from student.models import *
from django.contrib.auth.hashers import make_password,check_password
from django.core import serializers
import json
# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        registerNumber = request.POST['register_number']
        password = request.POST['password']
        regNo = RegisterModel.objects.filter(register_number=registerNumber)
        if not regNo:
            print("You are not register..Please register")
            return render(request, "loginpage", context={"messages" : "You are not register..Please register", "tags" : "warning"})
        else:
            user = serializers.serialize('json', regNo)
            data = json.loads(user)
            db_pass = data[0]['fields']['password']
            hashpass = check_password(password, db_pass)
            if hashpass:
                print("ok")
                return redirect("index")
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
                    email = email,
                    password = password)
                user.save()
                return redirect('loginpage')
            else:
                print("password Mismatched")
                return render(request, "student/registerPage.html", context={"messages" : "password mismated", "tags" : "danger"})
        else:
            print("User is already Registered")
    
    return render(request, "student/registerPage.html")



def indexPage(request):
    return render(request, "student/index.html")