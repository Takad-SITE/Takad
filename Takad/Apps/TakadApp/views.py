from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def index(request):
    
    return render(request,"url_result.html")