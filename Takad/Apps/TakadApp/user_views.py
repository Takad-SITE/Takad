from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *

#views for the homepage
def index(request): 
    if not request.session["UserLogedNaveBar"]:
        return redirect("/")
    try:
        theUserInfo = Users.objects.get(email=request.session["LogedEmail"])

        contex = {
            "user_firstname": theUserInfo.first_name,
            "user_lastName": theUserInfo.last_name,
            "user_Email": theUserInfo.email
        }

    except:
        # if error logout and displayer the main home
        request.session["UserLogedNaveBar"] = False
        return redirect("/")

    
    return render(request,"user_dashboard.html",contex)


def history(request):
        
    theUser_Reports = Reports_result.objects.filter (user=int(request.session["UserID"]))
    listUserREportArray =[]
    for theOneByOneReport in theUser_Reports :
       listUserREportArray.append( theOneByOneReport)



    contex = { "theUser_ReportsArray": listUserREportArray} 
    
    # for theOneByOneReport in theUser_Reports :
    #     dataScan_DB=theOneByOneReport.dict_report
    #     print(dataScan_DB)
        
    
    return render(request,"user_history.html",contex)
    

def showReportDetails (request,PK_ID_Report):

    if request.method == "POST":
        selected_Reports_Details_byID = Reports_result.objects.get(id=PK_ID_Report)
        dataReport=selected_Reports_Details_byID.dict_report
        return render(request, "url_result.html", dataReport)
    
    # whene he/she changed the URL minulayl redirect him to avoide minupulitaon and hackers maybe
    return redirect("/")

def DeleteReportDetails (request,PK_ID_Report):

    if request.method == "POST":
        selected_Reports_Details_byID = Reports_result.objects.get(id=PK_ID_Report)
        selected_Reports_Details_byID.delete()
        return redirect("/user/user_history")
    
    # whene he/she changed the URL minulayl redirect him to avoide minupulitaon and hackers maybe
    return redirect("/")

def contactus(request):
    return render(request,"user_contactus.html")
def contactus_form(request):
    return HttpResponse('Contact us form')