from django.urls import path

from . import views
from . import user_views
from . import admin_views

urlpatterns = [
    #urls for the homepage
    path('', views.index, name='index'),

    path('login',views.login),
    path('sign_up',views.sign_up),
    path('logout',views.logout),

    #to show PDF
    path('showPDF/<int:PK_ID_Report>',views.PDFReport),

    #urls for user dashboard
    path('user',user_views.index,name='user'), 
    path('user/user_history',user_views.history),
    path('user/user_contactus',user_views.contactus),
    path('user/SendMessageToAdmins',user_views.SendMessageToAdmins), # to send message to the Admins
    path('user/ReportDetails/<int:PK_ID_Report>',user_views.showReportDetails), # ali show spical report   # name="user/ReportDetails"
    path('user/ReportDetailsDelete/<int:PK_ID_Report>',user_views.DeleteReportDetails), # ali Delete report from histroy and DB
    
    # USER messages 
    path('user/userMsgView/<int:MsgID>',user_views.userMsgView),
    path('user/userMsgDelete/<int:MsgID>',user_views.userMsgDelete), 

    #urls for Admin dashboard
    path('admin',admin_views.index,name='admin'),
    path('admin/admin_dashboard_users',admin_views.admin_dashboard_users), 
    path('admin/admin_dashboard_msg',admin_views.admin_dashboard_msg),
    path('admin/ViewToReplayMsg/<int:MsgID>',admin_views.ViewToReplayMsg), 
    path('admin/ReplayMsg/<int:MsgID>',admin_views.ReplayMsg),
    path('admin/RemoveUser/<int:UserID>',admin_views.RemoveUser),
    
    #urls for result
    path('url_result',views.url_result),
    path('file_result',views.file_result),
]