from django.urls import path

from . import views
from . import user_views
from . import admin_views

urlpatterns = [
    #urls for the homepage
    path('', views.index, name='index'),
    path('login',views.login),
    path('sign_up',views.sign_up),

    # path('scan_url',views.scan_url),
    path('scan_file',views.scan_file),
    path('index2',views.index2),
    path('logout',views.logout),

    #urls for user dashboard
    path('user',user_views.index,name='user'), # path('user',user_views.index,name='user'),
    #path('logout',user_views.logout),
    path('user/user_history',user_views.history),
    path('user/user_contactus',user_views.contactus),
    path('user/contactus_form',user_views.contactus_form),
    path('user/ReportDetails/<int:PK_ID_Report>',user_views.showReportDetails), # ali show spical report   # name="user/ReportDetails"
    path('user/ReportDetailsDelete/<int:PK_ID_Report>',user_views.DeleteReportDetails), # ali Delete report from histroy and DB
    
    #urls for Admin dashboard
    path('admin',admin_views.index,name='admin'),
    #path('logout',admin_views.logout),
    path('admin/admin_dashboard_users',admin_views.admin_dashboard_users),
    path('admin/admin_dashboard_reports',admin_views.admin_dashboard_reports),
    path('admin/admin_dashboard_msg',admin_views.admin_dashboard_msg),
    path('admin/admin_dashboard_history',admin_views.admin_dashboard_history),
    
    #urls for result
    path('url_result',views.url_result),
    path('file_result',views.file_result),
]