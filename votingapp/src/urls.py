from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.baseResponse),

    path('profiles/', views.getProfiles),
    path('profiles/<str:pk>/', views.getProfile),

    path('groups/', views.getGroups),
    path('groups/<str:pk>/', views.getGroup),

    path('profiles-from-group/<str:pk>/', views.getAllProfilesFromGroup)
]
