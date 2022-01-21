from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.baseResponse),
    path('profiles/', views.getProfiles),
    path('profiles/<str:pk>', views.getProfile)
]
