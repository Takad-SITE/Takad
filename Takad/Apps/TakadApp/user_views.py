from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.messages import SUCCESS


def getUnReadMessages(request):
    totlaUnreadMessages = len(Messages.objects.filter(
        user=int(request.session["UserID"]), isRead=False))
    return totlaUnreadMessages


def getTOTMessages(request):
    getTOTMessages = len(Messages.objects.filter(
        user=int(request.session["UserID"])))
    return getTOTMessages

# views for the homepage


def index(request):
    if not request.session["UserLogedNaveBar"]:
        return redirect("/")
    try:
        theUserInfo = Users.objects.get(email=request.session["LogedEmail"])
        countHistoryNumber = Reports_result.objects.filter(
            user=int(request.session["UserID"]))
        contex = {
            "user_firstname": theUserInfo.first_name,
            "user_lastName": theUserInfo.last_name,
            "user_Email": theUserInfo.email,
            "numberOfReports": len(countHistoryNumber),
            "NumberOFUnreadMessages": getUnReadMessages(request),
            "NumberOfMessages": getTOTMessages(request)

        }

    except:
        # if error logout and displayer the main home
        request.session["UserLogedNaveBar"] = False
        return redirect("/")
    return render(request, "user_dashboard.html", contex)


def history(request):

    theUser_Reports = Reports_result.objects.filter(
        user=int(request.session["UserID"]))
    listUserREportArray = []
    for theOneByOneReport in theUser_Reports:
        listUserREportArray.append(theOneByOneReport)

    contex = {
        "theUser_ReportsArray": listUserREportArray,
        "NumberOFUnreadMessages": getUnReadMessages(request),
    }
    return render(request, "user_history.html", contex)


def showReportDetails(request, PK_ID_Report):

    if request.method == "POST":
        selected_Reports_Details_byID = Reports_result.objects.get(
            id=PK_ID_Report)
        dataReport = selected_Reports_Details_byID.dict_report
        
        # add PK_ID_Report in dictionary to use it in showPDF method ;)
        # i want the PK_ID_Report in PDF/Prient Button this why i appened it
        dataReport.update({"PK_ID_Report":PK_ID_Report})
        
        return render(request, "url_result.html", dataReport)

    # whene he/she changed the URL minulayl redirect him to avoide minupulitaon and hackers maybe
    return redirect("/")


def DeleteReportDetails(request, PK_ID_Report):

    if request.method == "POST":
        selected_Reports_Details_byID = Reports_result.objects.get(
            id=PK_ID_Report)
        selected_Reports_Details_byID.delete()
        messages.success(request, "The Report Has Been Deleted")
        return redirect("/user/user_history")

    # whene he/she changed the URL minulayl redirect him to avoide minupulitaon and hackers maybe
    return redirect("/")


def contactus(request):
    senderMessage = Messages.objects.filter(
        user=int(request.session["UserID"]))

    contex = {

        "NumberOFUnreadMessages": getUnReadMessages(request),
        "UserArrayMessages": senderMessage.values(),
    }
    return render(request, "user_contactus.html", contex)

# Send Message To Admins


def SendMessageToAdmins(request):
    # if not logedin go to home page
    if not request.session["UserLogedNaveBar"]:
        return redirect("/")
    # if get Post
    if request.method == "POST":
        # validation no empty  Title or Message
        if len(request.POST["userTitle"]) < 1 or len(request.POST["userMessage"]) < 1:
            messages.error(
                request, "Error: Please Enter the Title and the Message")
            return redirect("/user/user_contactus")  # not send
        else:
            # send
            senderID = Users.objects.get(id=int(request.session["UserID"]))
            Messages.objects.create(
                user=senderID, title=request.POST["userTitle"], message=request.POST["userMessage"])
            messages.success(request, "Message Has Been Send")
            return redirect("/user/user_contactus")
    # for hacker
    return redirect("/")


def userMsgView(request, MsgID):
    if request.method == "POST":
        messageDetials_byID = Messages.objects.get(id=MsgID)

        # updating
        # make it readis read = yes
        messageDetials_byID.isRead = True
        messageDetials_byID.save()
        contex = {
            "NumberOFUnreadMessages": getUnReadMessages(request),
            "MsgDetails": messageDetials_byID.__dict__
        }
        return render(request, "user_dashboard_mgs_show.html", contex)

    # whene he/she changed the URL minulayl redirect him to avoide minupulitaon and hackers maybe
    return redirect("/")


def userMsgDelete(request, MsgID):
    if request.method == "POST":
        message_byID = Messages.objects.get(id=MsgID)
        message_byID.delete()
        messages.success(request, "Message Deleted")
        return redirect("/user/user_contactus")

    # whene he/she changed the URL minulayl redirect him to avoide minupulitaon and hackers maybe
    return redirect("/")
