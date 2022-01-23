from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.baseResponse),

    path('users/', views.getUsers),
    path('users/<str:pk>/', views.getUser),

    path('groups/', views.getGroups),
    path('groups/<str:pk>/', views.getGroup),
]
