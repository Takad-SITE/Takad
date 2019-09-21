from django.shortcuts import render
from django.http import HttpResponse
from .models import *

#views for the homepage
def index(request): 
    return render(request,"admin_dashboard.html")
def logout(request):
    return HttpResponse('logout')
def admin_dashboard_users(request):
    return render(request,"admin_dashboard_users.html")
def admin_dashboard_reports(request):
    return render(request,"admin_dashboard_reports.html")
def admin_dashboard_msg(request):
    return render(request,"admin_dashboard_msg.html")