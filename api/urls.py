from django.contrib import admin
from django.urls import path, include

from api import views

# all students under a faculty
# all projects under a faculty
urlpatterns = [
    path('login/', views.login, name='login'),
    path('whoami/', views.whoami, name='whoami'),
    path('supervisor/request/', views.supervisor_requests, name='supervisor_requests'),
    path('faculty_incharge/request/', views.faculty_incharge_requests, name='faculty_incharge_requests'),
    path('lab_incharge/request/', views.lab_staff_requests, name='lab_incharge_requests'),
    path('supervisor/action/', views.take_action_supervisor, name='take_action_supervisor'),
    path('faculty_incharge/action/', views.take_action_faculty_incharge, name='take_action_faculty_incharge'),
    path('lab_incharge/action', views.take_action_lab_incharge, name='take_action_lab_incharge'),
    path('equipment/all', views.equipment_details, name='equipment_details'),
    path('slot/booked',views.booked_slots, name='project_details'),
    path('project/add_student', views.add_student_to_project, name='project_table_update'),
    path('profile/history',views.request_history,name='request_history'),
    path('profile/student_details',views.student_details,name='student_details'),
    path('profile/work_details', views.no_of_hours, name='no_of_hours'),
    path('request/', views.request_item, name='request_item'),
    path('request/pending/', views.pending_request_item, name='pending request_item'),
    path('equipment/add',views.add_equipment, name='add_project'),
    path('project/add',views.add_project, name='add_project'),
    path('equipment/repair',views.update_equipment_to_maintenance, name='add_equipment'),
    path('equipment/view', views.parse_equipment, name='parse_equipment'),
]
