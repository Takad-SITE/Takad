from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import requests  # for the API
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

        return redirect("/")
    else:
        # add new User

        theNewUser = Users.objects.create(first_name=request.POST["firstName_signUp"], last_name=request.POST["lastName_signUp"], email=str(
        request.POST["email_signUp"]).lower(), password=hashThisPassowrdForDB(request.POST["password_signUp"]), is_admin=False)
        theNewUser_ID = theNewUser.id  # get the new user ID

        # for loging (auto)
        request.session["LogedEmail"] = str(request.POST["email_signUp"]).lower()
        request.session["LogedID"] = theNewUser_ID
        request.session["UserLogedNaveBar"] = True

        messages.success(request, "A new User was added")
        print("_ _ _ oooooo ____",
              request.session["LogedID"], request.session["LogedEmail"])
        return redirect('/')


def login(request):
    if request.method == "GET":
        return redirect("/")

    # if loged / use dasheboard method maybe , ill checik this with my team  ( Ali)
    # if filtter() >==1 :
        # dashboard
    # __________________________________
    # Authintication
    # if not exisit in Database et error so this why i used try except
    try:
        theUserFromDB = Users.objects.get( email=str(request.POST["email_login"]))
        request.session["UserID"] =theUserFromDB.id # get the user ID form DB

        if checkPassowrd(str(request.POST["password_login"]), theUserFromDB.password):
            #lgoin = Authintication
            if theUserFromDB.is_admin == True:
                # loging as Admin
                request.session["LogedEmail"] = str( request.POST["email_login"]).lower()
                
                # for changeing the navebar
                request.session["UserLogedNaveBar"] = True
                return redirect("/")  # admin
            else:
                # loging as User
                # for changeing the navebar
                request.session["UserLogedNaveBar"] = True
                request.session["LogedEmail"] = str(request.POST["email_login"]).lower()
                
                return redirect("/")  # user
            #  return redirect("/login")
        else:
            # passowrd in correct ,but do not tell that for user, to avoide hacker
            request.session["UserLogedNaveBar"] = False
            messages.error(request, "Email or Password are incorrect")
            return render(request, "index.html")

    except:
        # can not login  , invialed Email or not register in DB
        messages.error(request, "Email or Password are incorrect")
        request.session["UserLogedNaveBar"] = False
        return render(request, "index.html")


# views for the homepage
def index(request):
    # if not exisit creat one witl  False value
    if "UserLogedNaveBar" not in request.session:
        request.session["UserLogedNaveBar"] = False

    # if loged in pass the useur info  , cuz need it in name and email
    if request.session["UserLogedNaveBar"] == True:
        try:
            theUserInfo = Users.objects.get(email=request.session["LogedEmail"])
            request.session["UserID"] =theUserInfo.id
            request.session["user_firstname"] = theUserInfo.first_name
            request.session["user_lastName"] = theUserInfo.last_name

        except:
            # if error logout and displayer the main home
            request.session["UserLogedNaveBar"] = False
            return render(request, "index.html")

        # display the loged user/Admin
        return render(request, "index.html")

    print("big render")
    return render(request, "index.html")


def index2(request):
    return render(request, "index2.html")


def logout(request):
    request.session["UserLogedNaveBar"] = False  # for changeing the navebar
    request.session["LogedEmail"] = ""  # rest the email session

    request.session["user_firstname"] = ""
    request.session["user_lastName"] = ""

    return render(request, "index.html")

# def scan_url(request):
#     return render(request, "url_result.html")


def scan_file(request):
    return HttpResponse('scan file')


def url_result(request):

    url = 'https://www.virustotal.com/vtapi/v2/url/scan'
    params = {'apikey': '570dd83555b7b7f4ba014db6ff59f3a2762c7a125417550abc1d70f542edc804',
              'url': request.POST['url']}
    responseScan = requests.post(url, data=params)
    dataScan = responseScan.json()
    # print(dataScan)

    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    params = {'apikey': '570dd83555b7b7f4ba014db6ff59f3a2762c7a125417550abc1d70f542edc804',
              'resource': dataScan['scan_id']}
    responseReport = requests.get(url, params=params)
    dataReport = responseReport.json()
    # print(dataReport)

    # Auto save in DB if loged in
    if request.session["UserLogedNaveBar"] == True:
         theUserInfo = Users.objects.get(id=int(request.session["UserID"]))
         theUserScannReport = Reports_result.objects.create( user=theUserInfo,dict_report=dataReport)
         print(" ------------------------------------- saved in DB -------------------------------------")

    return render(request, "url_result.html", dataReport)
    



def file_result(request):
    return render(request, "file_result.html")


# for page 404
def page404(request, exception):
    return render(request, "page404.html")
