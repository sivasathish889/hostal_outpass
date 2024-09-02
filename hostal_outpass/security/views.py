from django.shortcuts import render, redirect

# Create your views here.

def loginPage(request):
    return render(request, "security/index.html")