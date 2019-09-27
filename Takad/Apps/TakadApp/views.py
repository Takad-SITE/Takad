from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import requests  # for the API
from django.contrib import messages
from django.contrib.messages import SUCCESS, ERROR
# this for file
from django.core.files.storage import FileSystemStorage
# for limited API  scan in  minut
from json.decoder import JSONDecodeError
# for PDF
from .utils import render_to_pdf


def sign_up(request):
    # This is the Vaildation
    errors = Users.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect("/")
    else:
        # add new User

        theNewUser = Users.objects.create(first_name=request.POST["firstName_signUp"], last_name=request.POST["lastName_signUp"], email=str(
            request.POST["email_signUp"]).lower(), password=hashThisPassowrdForDB(request.POST["password_signUp"]), is_admin=False)
        theNewUser_ID = theNewUser.id  # get the new user ID

        # for loging (auto)
        request.session["LogedEmail"] = str(
            request.POST["email_signUp"]).lower()
        request.session["LogedID"] = theNewUser_ID
        request.session["UserLogedNaveBar"] = True

        messages.success(request, "You Have Been Signed Up Successfully")

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
        theUserFromDB = Users.objects.get(
            email=str(request.POST["email_login"]))
        request.session["UserID"] = theUserFromDB.id  # get the user ID form DB

        if checkPassowrd(str(request.POST["password_login"]), theUserFromDB.password):
            #lgoin = Authintication
            if theUserFromDB.is_admin == True:
                # loging as Admin
                # for changeing the navebar
                request.session["UserLogedNaveBar"] = True
                request.session["LogedEmail"] = str(
                    request.POST["email_login"]).lower()
                request.session["isItAdmin"] = theUserFromDB.is_admin  # True
                request.session["user_firstname"] = theUserFromDB.first_name
                request.session["user_lastName"] = theUserFromDB.last_name

                # this works for Admin only , becuz save  request.session["isItAdmin"] = True
                return redirect("/admin")

            else:
                # loging as User
                # for changeing the navebar
                request.session["UserLogedNaveBar"] = True
                request.session["LogedEmail"] = str(
                    request.POST["email_login"]).lower()
                request.session["isItAdmin"] = theUserFromDB.is_admin  # false
                return redirect("/")  # user
            #  return redirect("/login")
        else:
            # passowrd in correct ,but do not tell that for user, to avoide hacker
            request.session["UserLogedNaveBar"] = False
            messages.error(request, "Email or Password is Incorrect")
            return render(request, "index.html")

    except:
        # can not login  , invialed Email or not register in DB
        messages.error(request, "Email or Password is Incorrect")
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
            theUserInfo = Users.objects.get(
                email=request.session["LogedEmail"])
            request.session["UserID"] = theUserInfo.id
            request.session["user_firstname"] = theUserInfo.first_name
            request.session["user_lastName"] = theUserInfo.last_name
            request.session["isItAdmin"] = theUserInfo.is_admin

        except:
            # if error logout and displayer the main home
            request.session["UserLogedNaveBar"] = False
            return render(request, "index.html")

        # display the loged user/Admin
        return render(request, "index.html", {"isAdmin": request.session["isItAdmin"]})

    return render(request, "index.html")


def index2(request):
    return render(request, "index2.html")


def logout(request):
    request.session["UserLogedNaveBar"] = False  # for changeing the navebar
    request.session["LogedEmail"] = ""  # rest the email session

    request.session["user_firstname"] = ""
    request.session["user_lastName"] = ""
    request.session["isItAdmin"] = False
    return render(request, "index.html")

def url_result(request):
    try:
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

            # update some Value in DataReport
            # save File name in URL place in the dicounary

            dataReport['filescan_id'] = False  # make it always False for URL

            theUserInfo = Users.objects.get(id=int(request.session["UserID"]))
            theUserScannReport = Reports_result.objects.create(
                user=theUserInfo, dict_report=dataReport)
            #print(" ------------------------------------- saved in DB -------------------------------------")
    except JSONDecodeError:
            # Free API limited scan 4  time per min
        messages.error(request, "Please Wait for a Minute, Then Try Again")
        return redirect("/")
    except:
        # validation for uploded file
        messages.error(request, "Please Enter Valid URL")
        return redirect("/")

    # add PK_ID_Report in dictionary to use it in showPDF method ;)
    # i want the PK_ID_Report in PDF/Prient Button this why i appened it
    dataReport.update({"PK_ID_Report":Reports_result.objects.last().id}) # last one added cuz i am in it now  and to avoide an error
    
    return render(request, "url_result.html", dataReport)


def file_result(request):
    if request.method == 'POST':
        try:
            # in html name for the file inpute
            uploaded_file = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save("./files/"+uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(filename)

            urlScan = 'https://www.virustotal.com/vtapi/v2/file/scan'
            paramsScan = {
                'apikey': '570dd83555b7b7f4ba014db6ff59f3a2762c7a125417550abc1d70f542edc804'}
            files = {'file': (filename, open(filename, 'rb'))}
            responseScan = requests.post(
                urlScan, files=files, params=paramsScan)
            dataScan = responseScan.json()

            urlReport = 'https://www.virustotal.com/vtapi/v2/file/report'
            params = {'apikey': '570dd83555b7b7f4ba014db6ff59f3a2762c7a125417550abc1d70f542edc804',
                      'resource': dataScan['scan_id']}
            responseReport = requests.get(urlReport, params=params)
            dataReport = responseReport.json()

            # Auto save in DB if loged in and if there is an result  response_code = 1
            if request.session["UserLogedNaveBar"] == True and dataReport["response_code"] == 1:

                # update some Value in DataReport
                # save File name in URL place in the dicounary
                dataReport['url'] = uploaded_file.name
                # make it always True for Files
                dataReport['filescan_id'] = True

                theUserInfo = Users.objects.get(
                    id=int(request.session["UserID"]))
                theUserScannReport = Reports_result.objects.create(
                    user=theUserInfo, dict_report=dataReport)
                #print(" ------------------------------------- saved File Report in DB -------------------------------------")

        except JSONDecodeError:
            # Free API limited scan 4  time per min
            messages.error(request, "Please Wait for a Minute, Then Try Again")
            return redirect("/")

        except:
            # validation for uploded file
            messages.error(request, "Please Upload Your File First")
            return redirect("/")

    # add PK_ID_Report in dictionary to use it in showPDF method ;)
    # i want the PK_ID_Report in PDF/Prient Button this why i appened it
    dataReport.update({"PK_ID_Report":Reports_result.objects.last().id}) # last one added cuz i am in it now  and to avoide an error
    

    return render(request, "url_result.html", dataReport)

# for PDF
def PDFReport(request,PK_ID_Report):
    #this only for register users
    if request.method != 'POST':
        messages.error(request, "ليش تعدلها يدوي ؟ لقافه يعني ؟")
        return redirect("/")  

    if request.session["UserLogedNaveBar"] == True :
        selected_Reports_Details_byID = Reports_result.objects.get(id=PK_ID_Report)
        dataReport = selected_Reports_Details_byID.dict_report
        return render_to_pdf("PDF.html", dataReport)
    
    messages.error(request, "Please Login for Using PDFs Services")
    return redirect("/")  


# for page 404
def page404(request, exception):
    return render(request, "page404.html")
