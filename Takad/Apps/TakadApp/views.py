from django.shortcuts import render
from django.http import HttpResponse
from .models import *

#views for the homepage
def index(request): 
    return render(request,"index.html")
def login(request):
    return HttpResponse('hi')
def sing_up(request):
    return HttpResponse('sing_up')
def scan_url(request):
    return HttpResponse('scan url')
def scan_file(request):
    return HttpResponse('scan file')


def urls_result(request):
    return render(request,"url_result.html")

def file_result(request):
    return render(request,"file_result.html")
