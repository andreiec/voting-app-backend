from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

# Import token libraries
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('users', views.UserSet, basename='users')

urlpatterns = [
    path('groups/', views.getGroups),
    path('groups/<str:pk>/', views.getGroup),
    path('groups/<str:pk>/users/', views.getAllUsersFromGroup),

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
