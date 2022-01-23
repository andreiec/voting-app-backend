from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.baseResponse),


    path('groups/', views.getGroups),
    path('groups/<str:pk>/', views.getGroup),
]
