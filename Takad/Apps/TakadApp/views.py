from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import requests # for the API
from django.contrib import messages
from django.contrib.messages import SUCCESS, ERROR



def sign_up(request):
    # This is the Vaildation
    errors = Users.objects.basic_validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        print("error here ", "not validaitaion Adde alreat in html top left")
        
        return redirect("/") ## 
    else:
        # add new User

        theNewUser = Users.objects.create(first_name=request.POST["firstName_signUp"],last_name=request.POST["lastName_signUp"],email=str(request.POST["email_signUp"]).lower(),password=hashThisPassowrdForDB(request.POST["password_signUp"]),is_admin=False)
        theNewUser_ID = theNewUser.id #get the new user ID

        # for loging (auto)
        request.session["LogedEmail"] = str(request.POST["email_signUp"]).lower()
        request.session["LogedID"]= theNewUser_ID

        messages.success(request, "A new User was added")
        print("_ _ _ oooooo ____",request.session["LogedID"],request.session["LogedEmail"])
        return redirect('/') ##


def login(request):
    #if loged / use dasheboard method maybe , ill checik this with my team  ( Ali)
    # if filtter() >==1 : 
        # dashboard
    #__________________________________
    #Authintication 
    #if not exisit in Database et error so this why i used try except
    try:
        theUserFromDB=Users.objects.get(email=str(request.POST["email_login"]))
        if checkPassowrd(str(request.POST["password_login"]),theUserFromDB.password):
            #lgoin = Authintication
            if theUserFromDB.is_admin ==True: 
                #loging as Admin
                return HttpResponse("successful logiedin as Admin")
            else:
                #loging as User
                return HttpResponse("successful logiedin as USER")
            #  return redirect("/login")
        else:
        # passowrd in correct ,but do not tell that for user, to avoide hacker
            messages.error(request, "Email or Password are incorrect")
            return render(request,"index.html")
    
    except:
    #can not login  , invialed Email or not register in DB
        messages.error(request, "Email or Password are incorrect")
        return render(request,"index.html")
    


# views for the homepage
def index(request):
    return render(request, "index.html")

def index2(request):
    return render(request, "index2.html")
def logout(request):
    return redirect('/')

# def scan_url(request):
#     return render(request, "url_result.html")


def scan_file(request):
    return HttpResponse('scan file')


def url_result(request):
    
    url = 'https://www.virustotal.com/vtapi/v2/url/scan'
    params = {'apikey': '570dd83555b7b7f4ba014db6ff59f3a2762c7a125417550abc1d70f542edc804', 'url':request.POST['url']}
    responseScan = requests.post(url, data=params)
    dataScan = responseScan.json()
    # print(dataScan)

    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    params = {'apikey': '570dd83555b7b7f4ba014db6ff59f3a2762c7a125417550abc1d70f542edc804', 'resource':dataScan['scan_id']}
    responseReport = requests.get(url, params=params)
    dataReport = responseReport.json()
    # print(dataReport)

    return render(request, "url_result.html", dataReport)


def file_result(request):
    return render(request, "file_result.html")




#for page 404
def page404(request,exception):
    return render(request,"page404.html")