from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.messages import SUCCESS, ERROR

# get numberof Unreplayed messages for  Notivications and counnting messages number
def getNumberNewMessagesnotReplayedYet():
    UserMessageasHaveNotReplayedYet = Messages.objects.filter(
        replay="").values()
    return len(UserMessageasHaveNotReplayedYet)

# get Only Users Numbers without Admins


def GetOnlyUsersNumbers():
    CountUsersOnly = Users.objects.filter(is_admin=False).values()
    return len(CountUsersOnly)


def getOnlyAdminsNumber():
    CountAdminsOnly = Users.objects.filter(is_admin=True).values()
    return len(CountAdminsOnly)

# __________________________________________________________________________________

    # views for the homepage


def index(request):
    # if not admin do hot show the Admin's dashboard
    if request.session["isItAdmin"] == False:
        return redirect("/")

    # if admin Do ...

    TotalREports = len(Reports_result.objects.all())

    context = {
        "numberOfUnreplayedMessages": getNumberNewMessagesnotReplayedYet(),
        "AdminsNumberCounted":  getOnlyAdminsNumber(),
        "UsersNumberCounted": GetOnlyUsersNumbers(),
        "allReportsCounted": TotalREports,
        "user_firstname": request.session["user_firstname"],
        "user_lastName": request.session["user_lastName"],

    }

    return render(request, "admin_dashboard.html", context)


def logout(request):
    return HttpResponse('logout')


def admin_dashboard_users(request):
    # if not admin do hot show the Admin's dashboard
    if request.session["isItAdmin"] == False:
        return redirect("/")

    # if admin Do ...
    GetOnlyUsersInfo = Users.objects.filter(is_admin=False).values()
    print(len(GetOnlyUsersInfo))

    context = {
        "numberOfUnreplayedMessages": getNumberNewMessagesnotReplayedYet(),
        "UsersAccountsArray": GetOnlyUsersInfo,
        "UsersNumberCounted": GetOnlyUsersNumbers(),
    }
    return render(request, "admin_dashboard_users.html", context)


def admin_dashboard_msg(request):
    UserMessageasHaveNotReplayedYet = Messages.objects.filter(
        replay="").values()

    print("--------"*10)
    print(UserMessageasHaveNotReplayedYet,
          getNumberNewMessagesnotReplayedYet())  # removed this
    print("--------"*10)

    context = {
        "UsersMessegaesArray": UserMessageasHaveNotReplayedYet,
        "numberOfUnreplayedMessages": getNumberNewMessagesnotReplayedYet()
    }
    return render(request, "admin_dashboard_msg.html", context)


# Replay from Admin to message ( View )
def ViewToReplayMsg(request, MsgID):
    if request.method == "POST":
        messageDetials_byID = Messages.objects.get(id=MsgID)
        MsgDetails = messageDetials_byID.__dict__

        contex = {
            "numberOfUnreplayedMessages": getNumberNewMessagesnotReplayedYet(),
            "admin_firstname": request.session["user_firstname"],
            "admin_lastName": request.session["user_lastName"],
            "MsgDetails": MsgDetails,
        }
        return render(request, "admin_dashboard_msg_show.html", contex)

    # whene he/she changed the URL minulayl redirect him to avoide minupulitaon and hackers maybe
    return redirect("/")

def ReplayMsg(request, MsgID):
    if request.method == "POST":
        messageDetials_byID = Messages.objects.get(id=MsgID)
        # updating
        # make it readis read = False to show it to the User as Red after Replay
        messageDetials_byID.isRead = False
        messageDetials_byID.replay = request.POST["TheReplayMsg"] # update the REplay field in DB 
        messageDetials_byID.save()  # update = send (replay)
        messages.success(request, "Success Replayed to The User")
        return redirect("/admin/admin_dashboard_msg")
    # whene he/she changed the URL minulayl redirect him to avoide minupulitaon and hackers maybe
    return redirect("/")


def RemoveUser(request, UserID):
    if request.method == "POST":
        theUser = Users.objects.get(id=UserID)
        theUser.delete()
        messages.success(request, "The User Has Been Removed")
        return redirect("/admin/admin_dashboard_users") 

    # whene he/she changed the URL minulayl redirect him to avoide minupulitaon and hackers maybe
    return redirect("/")