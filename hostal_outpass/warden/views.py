from django.shortcuts import render

# Create your views here.
def loginPage(request):
    return render(request, "warden/loginPage.html")

def index(request):
    return render(request, 'warden/index.html')