from django.shortcuts import render,redirect
from student.models import *
from django.contrib.auth.hashers import make_password,check_password
from django.core import serializers
import json
from django.contrib import messages
import jwt
import random
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER

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
        # Check Exisits register Number in Database
        if not RegisterModel.objects.filter(register_number = register_number).exists():
            # To Check Password and Confrim Password
            if pass1 == pass2:
                # hashing password in django inbuilt method
                password = make_password(pass1)
                # New User Create
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


def loginPage(request):
    if request.method == 'POST':
        registerNumber = request.POST['register_number']
        password = request.POST['password']
        # Check Regsiter Number 
        regNo = RegisterModel.objects.filter(register_number=registerNumber)
        if not regNo:
            messages.warning(request,message="You are not register..Please register")
            return redirect('studentloginpage')
        else:
            user = serializers.serialize('json', regNo)
            data = json.loads(user)
            db_pass = data[0]['fields']['password']
            # check hashing Password
            hashpass = check_password(password, db_pass)
            # Check Password
            if hashpass:
                messages.success(request, "Login Successfully")
                res =  redirect("index")
                # Encoding user Data
                token = jwt.encode(payload=data[0],algorithm="HS256",key="secretKey")
                # Set the Cookie
                res.set_cookie('user', token)
                return res
            else:
                messages.warning(request ,message='Password Incorrect')
                return redirect('studentloginpage')

    return render(request, "student/loginPage.html")


def forget_password(request):
    if request.method == "POST":
        regNo = request.POST['regNo']
        # To Get register number data in db
        user = RegisterModel.objects.filter(register_number = regNo)
        user = serializers.serialize('json', user)
        data = json.loads(user)
        # check register number in db
        if not data :
            messages.warning(request, message="Register Number Wrong")
            return redirect('forgetpassword')
        else:
            # Generate random Otp
            otp = random.randint(10000,99999)
            to_mail = data[0]['fields']['email']
            # Email send 
            send_mail(
                subject="Reset Passeword",
                message=f"Your OTP is {otp}. This Is expierd in 5 minutes",
                recipient_list = [to_mail],
                from_email = EMAIL_HOST_USER
            )
            # hashing otp
            hashOTP = jwt.encode(payload={'otp' : otp},key="secret_key", algorithm='HS256')
            res = render(request, "student/confirmOTP.html", context= { "mail" : to_mail})
            # set Cookie in otp 
            res.set_cookie('otp', hashOTP, max_age=30000)
            return res
    return render(request, "student/forgetPassword.html")

def confirm_OTP(request):
        # to check otp in cookies
        if 'otp' in request.COOKIES.keys():
            cookie = request.COOKIES['otp']
            decodeData = jwt.decode(cookie, key="secret_key", algorithms="HS256")
            if request.method == 'POST':
                userOtp = request.POST['otp']
                otp = decodeData['otp']
                # check OTP
                if userOtp == otp:
                    messages.success(request, message="OTP verified")
                    res =  render(request, "student/changePassword.html")
                    # delete otp cookie 
                    res.delete_cookie('otp')
                    return res
                else:
                    messages.warning(request, message="Incorrect OTP.")
                    return redirect('confirmOTP')
            return render(request, "student/confirmOTP.html")
        else:
            messages.warning(request, message="Your OTP is Expired. Please resend OTP")
            return redirect('forgetpassword')

def logOut(request):
    messages.success(request, message='Logout Successfully')
    res =  render(request,'student/loginpage.html')
    # delete user cookie
    res.delete_cookie('user')
    return res


def indexPage(request):
    # to check user key in cookies
    if "user" in request.COOKIES.keys():
        cookie = request.COOKIES['user']
        # decode data 
        decodeData = jwt.decode(cookie, key="secretKey", algorithms="HS256")
        regNo = decodeData['fields']['register_number']
        # get user using register number
        user = RegisterModel.objects.filter(register_number = regNo)
        user = serializers.serialize('json', user)
        data = json.loads(user)
        db_pass = data[0]['fields'] 
        # convert data for template
        if db_pass['year'] == 1:
            years = 'First Year'
        elif db_pass['year'] == 2:
            years = 'Second Year'
        elif db_pass['year'] == 3:
            years = 'Third Year'
        else:
            years = 'Final Year'
        # reverse ordered data filtering in db requests 
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
        # create new Requests
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
    # decode data 
    decodeData = jwt.decode(cookie, key="secretKey", algorithms="HS256")
    regNo = decodeData['fields']['register_number']
    datas = RequestModel.objects.filter(regNo = regNo,pending__in = [2,3]).order_by('inTime').reverse()
    users = serializers.serialize('json', datas)
    dataa= json.loads(users)
    return render(request, 'student/preRequest.html', context={'reqData' : dataa})