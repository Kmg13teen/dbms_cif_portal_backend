from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('whoami/', views.whoami, name='whoami'),
    path('supervisor/request/', views.supervisor_requests, name='supervisor_requests'),
    path('faculty_incharge/request/', views.faculty_incharge_requests, name='faculty_incharge_requests'),
    path('lab_incharge/request/', views.lab_staff_requests, name='lab_incharge_requests'),
    path('supervisor/action/', views.take_action_supervisor, name='take_action_supervisor'),
    path('faculty_incharge/action/', views.take_action_faculty_incharge, name='take_action_faculty_incharge'),
    path('lab_incharge/action', views.take_action_lab_incharge, name='take_action_lab_incharge'),
]
