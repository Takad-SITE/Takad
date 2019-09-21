from django.shortcuts import render
from django.http import HttpResponse
from .models import *

#views for the homepage
def index(request): 
    return render(request,"user_dashboard.html")
def logout(request):
    return HttpResponse('logout')
def history(request):
    return render(request,"user_history.html")
def contactus(request):
    return render(request,"user_contactus.html")
def contactus_form(request):
    return HttpResponse('Contact us form')