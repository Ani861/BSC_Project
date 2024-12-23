from django.urls import path
from .import views 
from .views import login_view
from .views import index
from .views import add_schedule
from .views import teacher_list
from .views import add_teacher,report,report_view,User_report_view,User_report
from . import views

urlpatterns = [
    path('',views.login_view, name='login_view'),
    path('index/',views.index,name='index1'),
    path('add_schedule/',views.add_schedule, name='add_schedule'),
    path('add_teacher/',views.add_teacher, name='add_teacher'),
    path('delete_teacher/', views.delete_teacher, name='delete_teacher'),
    path('edit_teacher/<str:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('logout/', views.logout_view, name='logout'),
    path('assign_teacher/', views.assign_teacher, name='assign_teacher'),
    path('report', report, name='report'),
    path('report_view/',report_view,name='report_view'),
    path('User_report', User_report, name='User_report'),
    path('User_report_view/',User_report_view,name='User_report_view'),

]
